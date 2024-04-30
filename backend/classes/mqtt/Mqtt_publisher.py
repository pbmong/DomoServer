import time
import datetime

import paho.mqtt.client as mqtt

from libraries import database_access as ddbb

class Mqtt_publisher:

    # --- CONSTRUCTOR ---

    def __init__(self, mqtt_id, mqtt_broker_address, mqtt_broker_port):
               
        # MQTT client setup
        self.__mqtt_id = mqtt_id
        self.__mqtt_broker_address = mqtt_broker_address
        self.__mqtt_broker_port = mqtt_broker_port

    # --- PUBLIC METHODS ---

    def publish_message(self, messages_list):
        
        try:
            # Connecting to broker
            client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,self.__mqtt_id) #create new instance
            client.connect(self.__mqtt_broker_address, self.__mqtt_broker_port) #connect to broker

            # Publish messages to the topic
            for message_struct in messages_list:

                # Extracting message data [topic, message, delay]
                topic = message_struct[0]
                message = message_struct[1]
                delay = message_struct[2]
                db_update = message_struct[3]

                print("Publishing message to topic ", topic, message)
                
                client.publish(topic, message)

                if db_update == True:
                    try:
                        # Update ddbb
                        indexes = [x for x, v in enumerate(topic) if v == '/']

                        ddbb_table = topic[0:indexes[len(indexes)-1]]
                        ddbb_table = ddbb_table.replace('/','_')

                        # To update database with the new value
                        ddbb_meaning = topic[indexes[len(indexes)-1]+1:len(topic)]
                        query = F"UPDATE {ddbb_table} SET VALUE = '{message}' WHERE MEANING = '{ddbb_meaning}'"
                        print(query)
                        ddbb.ddbb_insert_query(query)

                        # To regist historic database with the new value
                        curr_dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        query = F"SELECT MAX(ID) FROM mqtt_historic"
                        result = ddbb.ddbb_select_query(query)
                        ID = result[0][0];
                        if ID == None:
                            ID = 0
                        query = F"INSERT INTO mqtt_historic (ID, DATETIME, TOPIC, VALUE) VALUES ('{ID + 1}','{curr_dt}', '{topic}', '{message}')"
                        ddbb.ddbb_insert_query(query)
                    except:
                        print("Error updating database")
                
                time.sleep(delay)

            client.disconnect()
        except Exception as e:
            print(f"Error connecting to broker {self.__mqtt_broker_address}:{self.__mqtt_broker_port} when publishing message with id {self.__mqtt_id}: {str(e)}")

        

        