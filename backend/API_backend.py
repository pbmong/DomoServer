# To execute API:  C:/Users/Usuario/AppData/Local/Microsoft/WindowsApps/python3.11.exe -m uvicorn backend.API_backend:app --reload
import subprocess
from fastapi import FastAPI



app = FastAPI()

@app.get("/update_parameter")
def update_parameter(topic = None, value = None):

    if topic is None or value is None:
        return "Values not provided. Please provide a topic and a value."
    else:
        #result = subprocess.run(['ls'])
        result = subprocess.run(['python', 'mqtt_send_to_topic_and_ddbb.py', topic, value], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return f"API response: {result.returncode, result.stdout, result.stderr}"

# python mqtt_send_to_topic_and_ddbb.py home/bedroom/L OFF