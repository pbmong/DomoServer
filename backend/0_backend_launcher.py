import subprocess


cmd_list = ["python /var/www/html/Domo/backend/ddbb_programed_commands.py",
 "python /var/www/html/Domo/backend/html_consult_url.py",
 "python /var/www/html/Domo/backend/mqtt_send_to_topic_and_ddbb.py home/room/R ON"]

for cmd in cmd_list:
    subprocess.Popen( ["lxterminal", "-e", cmd])

