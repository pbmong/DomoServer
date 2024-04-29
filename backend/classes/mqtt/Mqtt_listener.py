import os
import ftplib
import datetime

import paho.mqtt.client as mqtt
from libraries import database_access as ddbb


class Mqtt_listener:

    # --- ATTRIBUTES ---
    #FTP cam parameters
    CAMERA_TOPIC = "home/bedroom/C"

    #TODO: storage folder in ddbb configuration table
    files_download_folder = ""
    files_destiny_folder = "/files/"
    ftp_host = os.environ.get("FTP_PUBLICHOST","localhost")
    ftp_user = os.environ.get("FTP_USER_NAME","username")
    ftp_passwd = os.environ.get("FTP_USER_PASS","mypass")

    # --- CONTRUCTOR ---
    def __init__(self, mqtt_id, mqtt_bloker_address, mqtt_broker_port, topic_list):
        
        self.__client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, mqtt_id)
        self.__broker_address = mqtt_bloker_address
        self.__broker_port = mqtt_broker_port
        
        self.topic_list = topic_list
        self.__client.on_connect = self.__setup_connection

        self.__client.on_message = self.__process_message

    # --- PRIVATE METHODS ---

    def __setup_connection(self, client, userdata, flags, rc, properties=None):
        print(f"Connected with result code {rc}")
    
        for topic in self.topic_list:
            self.__client.subscribe(topic)

    def __process_message(self, client, userdata, message):
        msg_topic = message.topic
        msg_value = str(message.payload.decode("utf-8"))
        curr_dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')	
        print(f"({curr_dt}) {msg_topic}: {msg_value}")
        
        #update ddbb
        indexes = [x for x, v in enumerate(msg_topic) if v == '/']
        ddbb_table = msg_topic[0:indexes[len(indexes)-1]]
        ddbb_table = ddbb_table.replace('/','_')
        
        try:
            # Request processing
            # For camera
            if msg_topic == self.CAMERA_TOPIC:
                query = F"SELECT MAX(ID) FROM mqtt_historic"
                result = ddbb.ddbb_select_query(query)
                ID = result[0][0];
                if ID == None:
                    ID = 0
                query = F"INSERT INTO mqtt_historic (ID, DATETIME, TOPIC, VALUE) VALUES ('{ID + 1}','{curr_dt}', '{message.topic}', '{msg_value}')"
                ddbb.ddbb_insert_query(query)
                
                # If the message is an ACK, camera has sent all the images
                if msg_value == "ACK":
                    curr_dt = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
                    folder_destiny = self.files_destiny_folder + ddbb_table + "_"+ curr_dt + "/"
                    os.makedirs(folder_destiny)
                    
                    try:
                        # TODO: Define specific class for FTP client
                        # Get files from FTP container
                        print(f"Connecting to FTP server: {self.ftp_host} wirh user: {self.ftp_user}")
                        ftp_client = ftplib.FTP(host=self.ftp_host, user=self.ftp_user,passwd=self.ftp_passwd)  # connect to host, default port
                        
                        # Get list of all the files in the FTP server
                        ftp_files_list = ftp_client.nlst()
                        files_list = []           
                        for file in ftp_files_list:
                            # If the file is related to the topic
                            index = file.find(ddbb_table)
                            if index >= 0:
                                # Download file
                                dest_file = open(folder_destiny + file, 'wb')
                                ftp_client.retrbinary('RETR ' + file, dest_file.write)
                                ftp_client.delete(file)
                                dest_file.close()
                                files_list.append(file)

                        ftp_client.quit()

                        files = ""
                        for file in sorted(files_list):
                            files += " " + folder_destiny + file
                        print(f"Sending file: '{files_list}'")
                        os.system("python send_email.py 'Domotic Raspbian Service detected and intruder' " + files)

                    except Exception as e:
                        print(f"Error downloading files from FTP:" + str(e))

            # Default processing
            else:
                ddbb_meaning = msg_topic[indexes[len(indexes)-1]+1:len(msg_topic)]
                query = F"UPDATE {ddbb_table} SET VALUE = '{msg_value}' WHERE MEANING = '{ddbb_meaning}'"
                #print(query)
                ddbb.ddbb_insert_query(query)	

                query = F"SELECT MAX(ID) FROM mqtt_historic"
                result = ddbb.ddbb_select_query(query)
                ID = result[0][0];
                if ID == None:
                    ID = 0
                query = F"INSERT INTO mqtt_historic (ID, DATETIME, TOPIC, VALUE) VALUES ('{ID + 1}','{curr_dt}', '{message.topic}', '{msg_value}')"
                ddbb.ddbb_insert_query(query)    
                
        except Exception as e:
            print("MQTT message processing error:" + str(e))
    
    # --- PUBLIC METHODS ---

    def start(self):

        print("Starting MQTT listener to broker: " + self.__broker_address + ":" + str(self.__broker_port))
        self.__client.connect(self.__broker_address, self.__broker_port)
        self.__client.loop_forever()

    