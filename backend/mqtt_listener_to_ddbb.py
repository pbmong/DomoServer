import os

from libraries import database_access as ddbb
from classes.mqtt.Mqtt_listener import Mqtt_listener

topic_list = [	"home/living_room/P","home/living_room/T","home/living_room/H",
		        "home/bedroom/P","home/bedroom/T","home/bedroom/H","home/bedroom/C"]

# MQTT parameters
broker_address=os.environ.get("MQTT_CONTAINER_NAME", "localhost")
broker_port=1883
client_id = f'backend-listener-{os.getpid()}'

# MQTT listener setup
mqtt_listener = Mqtt_listener(client_id, broker_address, broker_port, topic_list)
mqtt_listener.start()


