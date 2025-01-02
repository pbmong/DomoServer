import os
import sys

from classes.mqtt.Mqtt_publisher import Mqtt_publisher

topic = sys.argv[1]
delay = int(sys.argv[2])

# MQTT parameters
broker_address=os.environ.get("MQTT_CONTAINER_NAME", "localhost")
broker_port=1883
client_id = f'backend-protocol-sunrise-{os.getpid()}'

# MQTT publisher setup

mqtt_publisher = Mqtt_publisher(client_id, broker_address, broker_port)

# command structure [topic, message, delay, db_update]
mqtt_commands_list =[
    [topic, "DOWN", delay, False],
    [topic, "DOWN", delay, False],
    [topic, "DOWN", delay, False],
    [topic, "DOWN", delay, False],
    [topic, "DOWN", delay, False],
    [topic, "DOWN", delay, False],
    [topic, "DOWN", delay, False],
    [topic, "DOWN", delay, False],
    [topic, "DOWN", delay, False],
    [topic, "DOWN", delay, False],
]


mqtt_publisher.publish_message(mqtt_commands_list)

