import urllib3

import mysql.connector
from mysql.connector import Error
import time
import datetime

url = "https://www.eltiempo.es/sevilla.html"

def get_url_data(url, substring_from, substring_to):

    http = urllib3.PoolManager()

    response = http.request('GET', url)

    f = open("demofile2.xml", "a")
    f.write(response.data.decode())
    f.close()

    ind_from = response.data.decode().find(substring_from)
    ind_to = response.data.decode().find(substring_to)

    try:
        url_dict = response.data.decode()[ind_from+len(substring_from) : ind_to-10]
        return url_dict[0:url_dict.find('\"')]
    
    except:
        print("Failed to parse xml from response ")
        return

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

        return mycursor.fetchall()
    except:
        print(f"DDBB error: {Error} ")


ambient_data = {'Temperatue': get_url_data(url, 'popup_temp_orig="','popup_temp="'),
                'Rain probability': get_url_data(url, 'popup_prob_rain_orig="','popup_prob_rain_text="')}

for data in ambient_data:              
    print(data + ": " + ambient_data[data])
