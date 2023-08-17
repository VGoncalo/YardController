import paho.mqtt.client as mqtt
import utils


def on_connect(client, userdata, flags, rc):
    client.subscribe("canteiroA/WaterStation/Pump")
    client.subscribe("canteiroA/WaterStation/DHT")
    client.subscribe("canteiroA/WaterStation/BS18D20")
    client.subscribe("canteiroA/EnvTracker/Soilhum")
    client.subscribe("canteiroB/WaterStation/Valve")
    client.subscribe("canteiroB/EnvTracker/Soilhum")
    client.subscribe("HealthChecker/temp")
    client.subscribe("HealthChecker/db")
    client.subscribe("HealthChecker/shutdown")
    utils.write_logs("Connect with result code "+str(rc), "on_connect")

def on_message(client, userdata, msg):
    log_msg = msg.payload.decode("utf-8","ignore")
    # events per topic
    if msg.topic == "canteiroA/WaterStation/Pump":
        log_msg = utils.prepare_data_for_insert(msg.topic, log_msg)
    if msg.topic == "canteiroA/WaterStation/BS18D20":
        print("canteiroA/WaterStation/WaterTemp ----> TBD")
    if msg.topic == "canteiroA/EnvTracker/Soilhum":
        print("canteiroA/EnvTracker/Soilhum ----> TBD")
        
    if msg.topic == "HealthChecker/temp":
        log_msg = utils.health_check_temp(msg.topic)
    if msg.topic == "HealthChecker/db":
        log_msg = utils.health_check_db(msg.topic)
    if msg.topic == "HealthChecker/shutdown":
        if msg.payload.decode("utf-8","ignore") == "Hello Rpi":
            print("Hello G,")
            print("vitler is about to close this connection")
            utils.tsleep(2)
            client.disconnect()
    else:
        # write to logs file
        utils.write_logs(log_msg, msg.topic)
    
def on_disconnect(client, userdata, flags, rc=0):
    utils.write_logs("Disconnected result code "+str(rc), "on_disconnect")
