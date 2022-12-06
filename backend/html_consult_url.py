import urllib3

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


ambient_data = {'temperatue': get_url_data(url, 'popup_temp_orig="','popup_temp="'),
                'rain probability': get_url_data(url, 'popup_prob_rain_orig="','popup_prob_rain_text="')}

for data in ambient_data:              
    print(data + ": " + ambient_data[data])