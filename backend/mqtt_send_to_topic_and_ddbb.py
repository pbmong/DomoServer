import os
import sys

from classes.mqtt.Mqtt_publisher import Mqtt_publisher


topic = sys.argv[1]
command =  sys.argv[2]

# MQTT parameters
broker_address=os.environ.get("MQTT_CONTAINER_NAME", "127.0.0.1")
broker_port=1883
client_id = f'backend-publisher-{os.getpid()}'

# MQTT publisher setup
mqtt_publisher = Mqtt_publisher(client_id, broker_address, broker_port)
mqtt_publisher.publish_message([[topic, command, 0, True]])

