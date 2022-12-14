import sys
import paho.mqtt.client as mqtt
import mysql.connector
from mysql.connector import Error

def ddbb_send_query(query):
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
        print(mycursor.rowcount, "record(s) affected")

    except:
        print(f"DDBB error: {Error} ")

############
def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
########################################

topic = sys.argv[1]
command = sys.argv[2]

# Send topic
broker_address="127.0.0.1"
#print("creating new instance")
client = mqtt.Client("P1") #create new instance
client.on_message=on_message #attach function to callback

#connecting to broker
client.connect(broker_address) #connect to broker
#client.loop_start() #start the loop
#Subscribing to topic Room/R
#client.subscribe("Room/R")
print("Publishing message to topic ", topic, command)

client.publish(topic, command)
client.disconnect()

#update ddbb
indexes = [x for x, v in enumerate(topic) if v == '/']
#print(indexes)

ddbb_table = topic[0:indexes[len(indexes)-1]]
ddbb_table = ddbb_table.replace('/','_')
#print(ddbb_table)

ddbb_meaning = topic[indexes[len(indexes)-1]+1:len(topic)]
#print(F"{ddbb_meaning}[{indexes[len(indexes)-1]+1}:{len(topic)}]")
query = F"UPDATE {ddbb_table} SET VALUE = '{command}' WHERE MEANING = '{ddbb_meaning}'"
print(query)
ddbb_send_query(query)

#client.loop_forever()
