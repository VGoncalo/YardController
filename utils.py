import os, time, subprocess
import datamodel as db

def write_logs(msg,topic):
    with open("logs/logs.txt","a", encoding="utf-8") as logfile:
        log_msg = time.asctime(time.localtime()) + " -- " + topic + " -- " + msg
        print("[LOG]: "+log_msg)
        logfile.write(f'{log_msg}\n')
        
def tsleep(x):
    return time.sleep(x)

def health_check_temp(topic):
    rpi_temp_cmd = subprocess.run("/usr/bin/vcgencmd measure_temp", shell=True, capture_output=True)
    rpi_temp = str(rpi_temp_cmd.stdout)
    return rpi_temp

def health_check_db(topic):
    isOK = db.check_db()
    return isOK

def prepare_data_for_insert(topic,val):
    canteiro = topic.split("/")[0]
    device = topic.split("/")[1]
    slave = topic.split("/")[2]
    new_value = {"device":device, "slave":slave, "value":val, "other":canteiro}
    record = db.insert_measurement(new_value) 
    return "record: "+str(record.inserted_id)+" value: "+val
    
