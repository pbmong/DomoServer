import os
import sys

from classes.mqtt.Mqtt_publisher import Mqtt_publisher
from libraries import database_access as ddbb


topic = sys.argv[1]
command =  sys.argv[2]

try:
    priority = sys.argv[3]
except:
    priority = 0

indexes = [x for x, v in enumerate(topic) if v == '/']
ddbb_table = topic[0:indexes[len(indexes)-1]]
ddbb_table = ddbb_table.replace('/','_')

# To update database with the new value
ddbb_meaning = topic[indexes[len(indexes)-1]+1:len(topic)]
query = F"SELECT LCP FROM {ddbb_table} WHERE MEANING = '{ddbb_meaning}'"
print(query)
result = ddbb.ddbb_select_query(query)  

if int(priority) >= result[0][0]:
    # MQTT parameters
    broker_address=os.environ.get("MQTT_CONTAINER_NAME", "127.0.0.1")
    broker_port=1883
    client_id = f'backend-publisher-{os.getpid()}'

    # MQTT publisher setup
    mqtt_publisher = Mqtt_publisher(client_id, broker_address, broker_port)
    mqtt_publisher.publish_message([[topic, command, priority, 0, True]])

