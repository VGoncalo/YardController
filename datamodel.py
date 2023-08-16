import pymongo, time
from pymongo import MongoClient

DB_URI = "mongodb://localhost:27017/"
DB_NAME = "home_server"

client = MongoClient(DB_URI)
home_serverdb = client[DB_NAME]
devices = None
measurements = None


def check_db_connection():
    if home_serverdb is None:
        return "ERROR: connection to mongodb"    
    else:
        return home_serverdb

def get_db_collections():
    collections = home_serverdb.list_collection_names()
    if "devices" in collections and "measurements" in collections:
        devices = home_serverdb["devices"]
        measurements = home_serverdb["measurements"]
        tables = {"devices":devices, "measurements":measurements}
        return tables
    else:
        return "ERROR: failed to get mongodb collections"

def insert_measurement(device, val):
	x = home_serverdb["measurements"].insert_one({"device":device,"value":val})
	print(x.inserted_id)

def health_check_db():
    try:
        # check devices
        devices_tab = home_serverdb["devices"]
        test_device = devices_tab.insert_one({"device":"DeviceHealthCheck","value":"TestValue"})
        devices_query = {"name":"DeviceHealthCheck"}
        deleted_devices = home_serverdb["devices"].delete_many(devices_query)
        query_devices_result = devices_tab.find(devices_query)
        # check measurements
        measure_tab = home_serverdb["measurements"]
        test_measure = measure_tab.insert_one({"data":time.asctime(time.localtime()),"device":"DeviceHealthCheck", "value":"heath-test-value"})
        measurements_query = {"device":"DeviceHealthCheck"}
        deleted_measure = home_serverdb["measurements"].delete_many(measurements_query)
        query_measure_result = measure_tab.find(measurements_query)
    except:
        print("ERROR: failed to perform check on mongo db")
    
    
