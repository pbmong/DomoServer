import os
import sys
import shutil

import time
import datetime

import paho.mqtt.client as mqtt
from libraries import database_access as ddbb

topic_list = [	"home/living_room/P","home/living_room/T","home/living_room/H",
		        "home/bedroom/P","home/bedroom/T","home/bedroom/H","home/bedroom/C"]

#FTP cam parameters
camera_topic = "home/bedroom/C"

#TODO: storage folder in ddbb configuration table
files_download_folder = "/home/pi/Downloads/"
files_upload_folder = "/var/www/html/Domo/backend/files/"

# MQTT parameters
broker_address=os.environ.get("MQTT_CONTAINER_NAME", "localhost")
broker_port=1883
client_id = f'backend-listener-{os.getpid()}'

def on_connect(client, userdata, flags, rc, properties=None):
    print(f"Connected with result code {rc}")
    
    for topic in topic_list:
        client.subscribe(topic)
    

def on_message(client, userdata, message):
    msg_topic = message.topic
    msg_value = str(message.payload.decode("utf-8"))
    curr_dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')	
    print(f"({curr_dt}) {msg_topic}: {msg_value}")
    
    #update ddbb
    indexes = [x for x, v in enumerate(msg_topic) if v == '/']
    ddbb_table = msg_topic[0:indexes[len(indexes)-1]]
    ddbb_table = ddbb_table.replace('/','_')
    
    try:
        #request processing
        #for camera
        if msg_topic == camera_topic:
            query = F"SELECT MAX(ID) FROM mqtt_historic"
            result = ddbb.ddbb_select_query(query)
            ID = result[0][0];
            if ID == None:
                ID = 0
            query = F"INSERT INTO mqtt_historic (ID, DATETIME, TOPIC, VALUE) VALUES ('{ID + 1}','{curr_dt}', '{message.topic}', '{msg_value}')"
            ddbb.ddbb_insert_query(query)
            
            # if the message is an ACK, camera has sent all the images
            if msg_value == "ACK":
                curr_dt = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                folder_destiny = files_upload_folder + ddbb_table + "_"+ curr_dt + "/"
                os.mkdir(folder_destiny)
                
                files_list = os.listdir(files_download_folder)
                for entry in files_list:
                    if entry.find(ddbb_table):
                        shutil.move(files_download_folder + entry,  folder_destiny + entry)
                files = ""
                for file in sorted(files_list):
                    files += " " + folder_destiny + file
                print(f"Sending file: '{files_list}'")
                os.system("python /var/www/html/Domo/backend/send_email.py 'Domotic Raspbian Service detected and intruder' " + files)


        #default processing
        else:
            ddbb_meaning = msg_topic[indexes[len(indexes)-1]+1:len(msg_topic)]
            query = F"UPDATE {ddbb_table} SET VALUE = '{msg_value}' WHERE MEANING = '{ddbb_meaning}'"
            #print(query)
            ddbb.ddbb_insert_query(query)	

            query = F"SELECT MAX(ID) FROM mqtt_historic"
            result = ddbb.ddbb_select_query(query)
            ID = result[0][0];
            if ID == None:
                ID = 0
            query = F"INSERT INTO mqtt_historic (ID, DATETIME, TOPIC, VALUE) VALUES ('{ID + 1}','{curr_dt}', '{message.topic}', '{msg_value}')"
            ddbb.ddbb_insert_query(query)    
            
    except:
        print("MQTT message processing error")


print("Starting MQTT listener to broker: " + broker_address + ":" + str(broker_port))
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id) #create new instance
client.on_message = on_message #attach function to callback
client.on_connect = on_connect

#connecting to broker
client.connect(broker_address,broker_port) #connect to broker

client.loop_forever()
