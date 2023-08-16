import paho.mqtt.client as mqtt
import utils


def on_connect(client, userdata, flags, rc):
    print("Connect with result code "+str(rc))
    client.subscribe("canteiroA/WaterStation/Pump")
    client.subscribe("canteiroA/WaterStation/DHT")
    client.subscribe("canteiroA/WaterStation/BS18D20")
    client.subscribe("canteiroA/EnvTracker/Soilhum")
    client.subscribe("canteiroB/WaterStation/Valve")
    client.subscribe("canteiroB/EnvTracker/Soilhum")
    client.subscribe("HealthChecker/db")
    client.subscribe("HealthChecker/shutdown")

def on_message(client, userdata, msg):
    utils.mqqt_dispatcher(client, userdata, msg)

def on_disconnect(client, userdata, flags, rc=0):
    print("Disconnected result code "+str(rc))
