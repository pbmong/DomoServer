import os
import sys
import shutil

import paho.mqtt.client as mqtt
import mysql.connector
from mysql.connector import Error
import time
import datetime

topic_list = [	"home/living_room/P","home/living_room/T","home/living_room/H",
		"home/bedroom/P","home/bedroom/T","home/bedroom/H","home/bedroom/C"]

#FTP cam parameters
files_download_folder = "/home/pi/Downloads/"
files_upload_folder = "/var/www/html/Domo/files/"

def ddbb_insert_query(query):
    try: 
        mydb = mysql.connector.connect(
        host = "localhost",
        user = "pi",
        password = "raspberry",
        database = "DomoServer"
        )

        mycursor = mydb.cursor()
        mycursor.execute(query)
        mydb.commit()
        # print(mycursor.rowcount, "record(s) affected")

    except:
        print(f"DDBB error: {Error} ")

def ddbb_select_query(query):
    try: 
        mydb = mysql.connector.connect(
        host = "localhost",
        user = "pi",
        password = "raspberry",
        database = "DomoServer"
        )

        mycursor = mydb.cursor()
        mycursor.execute(query)

        return mycursor.fetchall()
    except:
        print(f"DDBB error: {Error} ")


def on_connect(client, userdata, flags, rc):
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
    
    #request processing
    #for camera
    if msg_topic == "home/bedroom/C":
        query = F"SELECT MAX(ID) FROM mqtt_historic"
        result = ddbb_select_query(query)
        ID = result[0][0];
        if ID == None:
            ID = 0
        query = F"INSERT INTO mqtt_historic (ID, DATETIME, TOPIC, VALUE) VALUES ('{ID + 1}','{curr_dt}', '{message.topic}', '{msg_value}')"
        ddbb_insert_query(query)
        
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
            os.system("python /var/www/html/Domo/backend/send_email.py 'Domotic Raspbian Service detecte and intruder' " + files)


    #default processing
    else:
        ddbb_meaning = msg_topic[indexes[len(indexes)-1]+1:len(msg_topic)]
        query = F"UPDATE {ddbb_table} SET VALUE = '{msg_value}' WHERE MEANING = '{ddbb_meaning}'"
        #print(query)
        ddbb_insert_query(query)	

        query = F"SELECT MAX(ID) FROM mqtt_historic"
        result = ddbb_select_query(query)
        ID = result[0][0];
        if ID == None:
            ID = 0
        query = F"INSERT INTO mqtt_historic (ID, DATETIME, TOPIC, VALUE) VALUES ('{ID + 1}','{curr_dt}', '{message.topic}', '{msg_value}')"
        ddbb_insert_query(query)


# Send topic
broker_address="127.0.0.1"
#print("creating new instance")
client = mqtt.Client("esp8266-client-") #create new instance
client.on_message=on_message #attach function to callback
client.on_connect = on_connect

#connecting to broker
client.connect(broker_address) #connect to broker

client.loop_forever()
