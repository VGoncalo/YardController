import os, time
import datamodel as db


def write_logs(msg,topic):
    with open("logs/logs.txt","a", encoding="utf-8") as logfile:
        log_msg = time.asctime(time.localtime()) + "--" + topic + "--" + msg
        logfile.write(f'{log_msg}\n')
        print("[LOG]: "+log_msg)

def mqqt_dispatcher(client, userdata, msg):
    if msg.topic == "canteiroA/WaterStation/Pump":
        db.insert_measurement(msg.topic, msg.payload.decode("utf-8","ignore"))
    if msg.topic == "canteiroA/EnvTracker/Soilhum":
        db.insert_measurement(msg.topic, msg.payload.decode("utf-8","ignore"))
    if msg.topic == "HealthChecker/db":
        health_check_db(msg.topic) 
    if msg.topic == "HealthChecker/shutdown":
        if msg.payload.decode("utf-8","ignore") == "Hello Rpi":
            print("Hello G,")
            print("vitler is about to close this connection")
            time.sleep(2)
            client.disconnect()
    
def health_check_db(topic):
    db.health_check_db()
    
