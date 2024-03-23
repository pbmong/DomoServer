import sys
import urllib3
import time
import datetime

from libraries import database_access as ddbb

str_err = "Url parsing error"

dic_data = sys.argv[1]
url = sys.argv[2]
find_from = sys.argv[3]
find_to = sys.argv[4]
sub_url_form = sys.argv[5]
sub_url_to = sys.argv[6]
consulting_delay = int(sys.argv[7])


def get_url_data(url, sub_url_form, sub_url_to, substring_from, substring_to):

    try:    
        http = urllib3.PoolManager()

        response = http.request('GET', url)
        decoded_data = response.data.decode('utf-8') #, errors='replace'
    
        #f = open("demofile2.xml", "a")
        #f.write(response.data.decode())
        #f.close()
    
        ind_sub_from = decoded_data.find(sub_url_form)
        ind_sub_to = decoded_data.find(sub_url_to)

        sub_url = decoded_data[ind_sub_from+len(sub_url_form) : ind_sub_to]
        # print("sub_url[" + str(ind_sub_from) + ":" + str(ind_sub_to) + "]:")

        ind_from = sub_url.find(substring_from)
        sub_url = sub_url[ind_from+len(substring_from) : ind_from+len(substring_from) + 200]
        # print("sub_url["+ str(ind_from) +":-]: "+sub_url)
        ind_to = sub_url.find(substring_to)
    
        url_dict = sub_url[0 : ind_to]
        return url_dict
    
    except:
        print("Failed to receive data from url ")
        return str_err


while(True):
    ambient_data = {dic_data: get_url_data(url, sub_url_form, sub_url_to, find_from, find_to)}    
    consulting_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    print("---- Data updating ("+consulting_datetime+") ----")
    if ambient_data[dic_data] == str_err:
        print(ambient_data[dic_data])
    else:
        print(dic_data + "["+ str(len(ambient_data[dic_data])) +"]: "+ ambient_data[dic_data])
        query = F"UPDATE home_external SET VALUE = '{ambient_data[dic_data]}', DATETIME = '{consulting_datetime}' WHERE MEANING = '{dic_data}'"
        ddbb.ddbb_update_query(query)
	
    time.sleep(consulting_delay)