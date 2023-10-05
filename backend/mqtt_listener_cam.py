import os
import sys
import shutil

import paho.mqtt.client as mqtt
import mysql.connector
from mysql.connector import Error
import time
import datetime

topic_list = [	"home/bedroom/C"]
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
    curr_dt = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')	
    print(f"({curr_dt}) {msg_topic}: {msg_value}")
    
    #update ddbb
    indexes = [x for x, v in enumerate(msg_topic) if v == '/']
    ddbb_table = msg_topic[0:indexes[len(indexes)-1]]
    ddbb_table = ddbb_table.replace('/','_')

    #manage images
    if msg_value == "ACK":
        folder_destiny = files_upload_folder + ddbb_table + "_"+ curr_dt + "/"
        os.mkdir(folder_destiny)
        entries = os.listdir(files_download_folder)
        for entry in entries:
            print(f"Sending file: '{entry}'")
            if entry.find(ddbb_table):
                shutil.move(files_download_folder + entry,  folder_destiny + entry)
                os.system("python /var/www/html/Domo/backend/send_email.py 'Domotic Raspbian Service detecte and intruder' " + folder_destiny + entry)
    


# Send topic
broker_address="127.0.0.1"
#print("creating new instance")
client = mqtt.Client("esp8266-client-") #create new instance
client.on_message=on_message #attach function to callback
client.on_connect = on_connect

#connecting to broker
client.connect(broker_address) #connect to broker

client.loop_forever()
