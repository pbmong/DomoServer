import urllib3
import mysql.connector
from mysql.connector import Error
import time
import datetime

url = "https://www.google.com/search?q=el+tiempo+sevilla&oq=el+tiempo+sevilla"
url = "https://www.eltiempo.es/sevilla.html"

def get_url_data(url, substring_from, substring_to):

    http = urllib3.PoolManager()

    response = http.request('GET', url)

    #f = open("demofile2.xml", "a")
    #f.write(response.data.decode("UTF-8"))
    #f.close()

    ind_sub_from = response.data.decode().find('<section class="block_full row_box row_number_2" >')
    ind_sub_to = response.data.decode().find('<section class="block_full row_box row_number_3" >')
    
    sub_url = response.data.decode()[ind_sub_from+len(substring_from) : ind_sub_to]

    ind_from = sub_url.find(substring_from)
    sub_url = sub_url[ind_from+len(substring_from) : len(sub_url)]
    ind_to = sub_url.find(substring_to)

    try:
        url_dict = sub_url[0 : ind_to]
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
        mydb.commit()
        print(mycursor.rowcount, "record(s) affected")

    except:
        print(f"DDBB error: {Error} ")

ambient_data = {'Temperature': get_url_data(url, '<span class="c-tib-text" data-temp="','°</span>"')}

while(True):
    consulting_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    print("---- Data updating ("+consulting_datetime+") ----")

    for data in ambient_data:              
        print(data + "["+ str(len(ambient_data[data])) +"]: " + ambient_data[data])
        query = F"UPDATE home_external SET VALUE = '{ambient_data[data]}', DATETIME = '{consulting_datetime}' WHERE MEANING = '{data}'"
        ddbb_send_query(query)
	
    time.sleep(300)
