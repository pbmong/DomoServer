import os
import sys
import paho.mqtt.client as mqtt
import time
import datetime

from libraries import database_access as ddbb

############
def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
########################################

topic = sys.argv[1]
command = sys.argv[2]

# MQTT parameters
broker_address=os.environ.get("MQTT_CONTAINER_NAME", "localhost")
broker_port=1883
client_id = f'backend-publisher-{os.getpid()}'

# MQTT client setup
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id) #create new instance
client.on_message=on_message #attach function to callback

try:
# Connecting to broker
    client.connect(broker_address) #connect to broker
    print("Publishing message to topic ", topic, command)

    client.publish(topic, command)
    client.disconnect()
except:
    print("Error connecting to broker when publishing message")

# Update ddbb
indexes = [x for x, v in enumerate(topic) if v == '/']

ddbb_table = topic[0:indexes[len(indexes)-1]]
ddbb_table = ddbb_table.replace('/','_')

# To update database with the new value
ddbb_meaning = topic[indexes[len(indexes)-1]+1:len(topic)]
query = F"UPDATE {ddbb_table} SET VALUE = '{command}' WHERE MEANING = '{ddbb_meaning}'"
print(query)
ddbb.ddbb_insert_query(query)

# To regist historic database with the new value
curr_dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
query = F"SELECT MAX(ID) FROM mqtt_historic"
result = ddbb.ddbb_select_query(query)
ID = result[0][0];
if ID == None:
    ID = 0
query = F"INSERT INTO mqtt_historic (ID, DATETIME, TOPIC, VALUE) VALUES ('{ID + 1}','{curr_dt}', '{topic}', '{command}')"
ddbb.ddbb_insert_query(query)

