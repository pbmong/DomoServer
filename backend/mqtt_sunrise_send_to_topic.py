import sys
import paho.mqtt.client as mqtt
import mysql.connector
from mysql.connector import Error
import time
import datetime


def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)

#############

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

#############

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

##########################################

topic = sys.argv[1]
delay = int(sys.argv[2])

broker_address="127.0.0.1"
client = mqtt.Client("P1") #create new instance
client.on_message=on_message #attach function to callback

client.connect(broker_address) #connect to broker
print("Publishing message to topic ",topic)

client.publish(topic,"ON")
ind = range(0,10)
for i in ind:
    client.publish(topic,"UP")
    time.sleep(delay)
client.disconnect()

#update ddbb
indexes = [x for x, v in enumerate(topic) if v == '/']
#print(indexes)

ddbb_table = topic[0:indexes[len(indexes)-1]]
ddbb_table = ddbb_table.replace('/','_')
#print(ddbb_table)

ddbb_meaning = topic[indexes[len(indexes)-1]+1:len(topic)]
#print(F"{ddbb_meaning}[{indexes[len(indexes)-1]+1}:{len(topic)}]")
query = F"UPDATE {ddbb_table} SET VALUE = 'ON' WHERE MEANING = '{ddbb_meaning}'"
print(query)
ddbb_insert_query(query)

curr_dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
query = F"SELECT MAX(ID) FROM mqtt_historic"
result = ddbb_select_query(query)
ID = result[0][0];
if ID == None:
    ID = 0
query = F"INSERT INTO mqtt_historic (ID, DATETIME, TOPIC, VALUE) VALUES ('{ID + 1}','{curr_dt}', '{topic}', 'ON')"
ddbb_insert_query(query)