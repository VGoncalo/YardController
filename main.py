#!/usr/bin/env python3

import utils
import mqttbroker as mos
import datamodel as db


# prepare the database models
try:
    db_client = db.check_db_connection()
    db_tables = db.get_db_collections()
except:
	print("Error on db connection")


# start the mqqt broker
devices_channel = mos.mqtt.Client()
devices_channel.connect("192.168.0.38", 1883, 60)
devices_channel.on_connect = mos.on_connect
devices_channel.on_message = mos.on_message
devices_channel.on_disconnect = mos.on_disconnect
devices_channel.loop_forever()
