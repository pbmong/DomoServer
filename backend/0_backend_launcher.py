import subprocess

#"sudo systemctl restart mosquitto"

#commands launching to start backend services
cmd_list = [

"python /var/www/html/Domo/backend/ddbb_programed_commands.py",
"python /var/www/html/Domo/backend/mqtt_listener_to_ddbb.py",	 

"python /var/www/html/Domo/backend/weather_api_consult.py",
]

for cmd in cmd_list:
    subprocess.Popen( ["lxterminal", "-e", cmd])

