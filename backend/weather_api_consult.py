import sys
import urllib3
import time
import datetime

import json

from libraries import database_access as ddbb

str_err = "Url parsing error"

dic_data = "ambient_data"
url = "https://www.el-tiempo.net/api/json/v2/provincias/41/municipios/41091"
consulting_delay = 5000


def get_url_data(url):

    try:    
        http = urllib3.PoolManager()

        response = http.request('GET', url)
        
        return response.json();
    
    except Exception:
        print("Error getting data from url: ")
        print(Exception)
        return str_err


while(True):
    weather_response = get_url_data(url)  
    consulting_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    print("---- Data updating ("+consulting_datetime+") ----")
    if weather_response == str_err:
        print(weather_response)
    else:
        try:
            if weather_response["municipio"]["NOMBRE"] == "Sevilla":
                current_temperature = weather_response["temperatura_actual"]
                sunset = weather_response["pronostico"]["hoy"]["@attributes"]["orto"]
                sunrise = weather_response["pronostico"]["hoy"]["@attributes"]["ocaso"]

                try:
                    query = F"UPDATE home_external SET VALUE = '{current_temperature}', DATETIME = '{consulting_datetime}' WHERE MEANING = 'Temperature'"
                    ddbb.ddbb_update_query(query)

                    query = F"UPDATE home_external SET VALUE = '{sunset}', DATETIME = '{consulting_datetime}' WHERE MEANING = 'Sunset'"
                    ddbb.ddbb_update_query(query)

                    query = F"UPDATE home_external SET VALUE = '{sunrise}', DATETIME = '{consulting_datetime}' WHERE MEANING = 'Sunrise'"
                    ddbb.ddbb_update_query(query)  
                except: 
                    print("Error updating weather data in database")     
            else:
                print("Weather data not from Sevilla")
            
        except:
            print("Error processing weather json data")
	
    time.sleep(consulting_delay)