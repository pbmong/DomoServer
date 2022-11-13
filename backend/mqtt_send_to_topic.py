import paho.mqtt.client as mqtt
import sys


############
def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
########################################

broker_address="127.0.0.1"
#print("creating new instance")
client = mqtt.Client("P1") #create new instance
client.on_message=on_message #attach function to callback

#connecting to broker
client.connect(broker_address) #connect to broker
#client.loop_start() #start the loop
#Subscribing to topic Room/R
#client.subscribe("Room/R")
print("Publishing message to topic ",sys.argv[1],sys.argv[2])

client.publish(sys.argv[1],sys.argv[2])
client.disconnect()

#client.loop_forever()
