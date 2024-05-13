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

# API to insert a command into the database
@app.get("/insert_command")
def insert_command(command = None, datetime = None, weekday = None):
    if command is datetime or weekday is None:
        return "Command para not provided"
    else:
        operation = "Insert"
        result = subprocess.run(['python', 'ddbb_commands_management.py', operation, command, datetime, weekday], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return f"API response: {result.returncode, result.stdout, result.stderr}"
    
# API to delete a command from the database
@app.get("/delete_command")
def delete_command(command_id = None):
    if command_id is None:
        return "Command ID not provided"
    else:
        operation = "Delete"
        result = subprocess.run(['python', 'ddbb_commands_management.py', operation, command_id], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return f"API response: {result.returncode, result.stdout, result.stderr}"