import sys
import paho.mqtt.client as mqtt
import time
import datetime

from libraries import database_access as ddbb

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)

#############

topic = sys.argv[1]
delay = int(sys.argv[2])

broker_address="127.0.0.1"
client = mqtt.Client("P1") #create new instance
client.on_message=on_message #attach function to callback

client.connect(broker_address) #connect to broker
print("Publishing message to topic ",topic)

#client.publish(topic,"ON")
ind = range(0,10)
for i in ind:
    client.publish(topic,"DOWN")
    time.sleep(delay)
#client.publish(topic,"OFF")
client.disconnect()

#update ddbb
#indexes = [x for x, v in enumerate(topic) if v == '/']

#ddbb_table = topic[0:indexes[len(indexes)-1]]
#ddbb_table = ddbb_table.replace('/','_')

#ddbb_meaning = topic[indexes[len(indexes)-1]+1:len(topic)]
#query = F"UPDATE {ddbb_table} SET VALUE = 'OFF' WHERE MEANING = '{ddbb_meaning}'"
#ddbb.ddbb_insert_query(query)

#curr_dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#query = F"SELECT MAX(ID) FROM mqtt_historic"
#result = ddbb_select_query(query)
#ID = result[0][0];
#if ID == None:
#    ID = 0
#query = F"INSERT INTO mqtt_historic (ID, DATETIME, TOPIC, VALUE) VALUES ('{ID + 1}','{curr_dt}', '{topic}', 'OFF')"
#ddbb.ddbb_insert_query(query)
