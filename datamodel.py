import pymongo, time
from pymongo import MongoClient

DB_URI = "mongodb://localhost:27017/"
DB_NAME = "yard_data_collection"

client = MongoClient(DB_URI)
data = client[DB_NAME]


def check_db_connection():
    if data is None:
        return "ERROR: connection to mongodb"    
    else:
        return data

def get_db_collections():
    collections = data.list_collection_names()
    if "messages" in collections:
        measurements = data["messages"]
        return measurements
    else:
        return "ERROR: failed to get mongodb collections"

def insert_measurement(record):
    try:
        rec = data["messages"].insert_one(record)
        return rec
    except Exception as e:
        return str(e)

def check_db():
    try:
        data_table = data["messages"]
        test_entry = data_table.insert_one({"device":"DeviceHealthCheck","value":"TestValue"})
        devices_query = {"device":"DeviceHealthCheck"}
        deleted_devices = data["messages"].delete_many(devices_query)
        query_devices_result = data_table.find(devices_query)
        return "mongodb is OK"
    except Exception as e:
        return "ERROR: db is KO" + str(e)
    
    
