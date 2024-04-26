import os
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

# MQTT parameters
broker_address=os.environ.get("MQTT_CONTAINER_NAME", "localhost")
broker_port=1883
client_id = f'backend-protocol-sunset-{os.getpid()}'

# MQTT client setup
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id) #create new instance
client.on_message=on_message #attach function to callback

client.connect(broker_address) #connect to broker
print("Publishing message to topic ",topic)

# Publish messages to the topic
ind = range(0,10)
for i in ind:
    client.publish(topic,"DOWN")
    time.sleep(delay)
    
client.disconnect()

