import sys
import urllib3
import mysql.connector
from mysql.connector import Error
import time
import datetime


dic_data = sys.argv[1]
url = sys.argv[2]
find_from = sys.argv[3]
find_to = sys.argv[4]
sub_url_form = sys.argv[5]
sub_url_to = sys.argv[6]
consulting_delay = int(sys.argv[7])


def get_url_data(url, sub_url_form, sub_url_to, substring_from, substring_to):

    http = urllib3.PoolManager()

    response = http.request('GET', url)
    decoded_data = response.data.decode('utf-8') #, errors='replace'
    f = open("demofile2.xml", "a")
    f.write(decoded_data)
    f.close()

    ind_sub_from = decoded_data.find(sub_url_form)
    ind_sub_to = decoded_data.find(sub_url_to)
    
    sub_url = decoded_data[ind_sub_from+len(sub_url_form) : ind_sub_to]
    # print("sub_url[" + str(ind_sub_from) + ":" + str(ind_sub_to) + "]:")

    ind_from = sub_url.find(substring_from)
    sub_url = sub_url[ind_from+len(substring_from) : ind_from+len(substring_from) + 200]
    # print("sub_url["+ str(ind_from) +":-]: "+sub_url)
    ind_to = sub_url.find(substring_to)

    try:
        url_dict = sub_url[0 : ind_to]
        return url_dict
    
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

while(True):
    ambient_data = {dic_data: get_url_data(url, sub_url_form, sub_url_to, find_from, find_to)}    

    consulting_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    print("---- Data updating ("+consulting_datetime+") ----")

    for data in ambient_data:              
        print(data + "["+ str(len(ambient_data[data])) +"]: "+ ambient_data[data])
        query = F"UPDATE home_external SET VALUE = '{ambient_data[data]}', DATETIME = '{consulting_datetime}' WHERE MEANING = '{data}'"
        ddbb_send_query(query)
	
    time.sleep(consulting_delay)
