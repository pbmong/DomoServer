# To execute API:  C:/Users/Usuario/AppData/Local/Microsoft/WindowsApps/python3.11.exe -m uvicorn backend.API_backend:app --reload
import subprocess
from fastapi import FastAPI



app = FastAPI()

# API to update a parameter in the database and send it to the MQTT broker
@app.get("/update_parameter")
def update_parameter(topic = None, value = None):

    if topic is None or value is None:
        return "Values not provided. Please provide a topic and a value."
    else:
        result = subprocess.run(['python', 'mqtt_send_to_topic_and_ddbb.py', topic, value], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return f"API response: {result.returncode, result.stdout, result.stderr}"
    
# API to execute the sunset protocol and send the data to the MQTT broker
@app.get("/protocol_sunset")
def protocol_sunset(topic = None):
    if topic is None:
        return "Values not provided. Please provide a topic."
    else:
        result = subprocess.run(['python', 'protocol_mqtt_sunset_send_to_topic.py', topic, "1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return f"API response: {result.returncode, result.stdout, result.stderr}"

# API to execute the sunrise protocol and send the data to the MQTT broker
@app.get("/protocol_sunrise")
def protocol_sunrise(topic = None):
    if topic is None:
        return "Values not provided. Please provide a topic."
    else:
        result = subprocess.run(['python', 'protocol_mqtt_sunrise_send_to_topic.py', topic, "1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return f"API response: {result.returncode, result.stdout, result.stderr}"