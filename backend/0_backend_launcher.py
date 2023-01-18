import subprocess 


cmd_list = ["python /var/www/html/Domo/backend/ddbb_programed_commands.py",

 """python /var/www/html/Domo/backend/html_consult_url.py Temperature https://www.eltiempo.es/sevilla.html '<span class="c-tib-text" data-temp="' '">' '<section class="block_full row_box row_number_2" >' '<section class="block_full row_box row_number_3" >' 900""",
 "python /var/www/html/Domo/backend/html_consult_url.py Sunrise https://www.timeanddate.com/sun/spain/sevilla '<tr><th>Sunrise Today: </th><td>' '<span ' 'body' '/body' 86400",
 "python /var/www/html/Domo/backend/html_consult_url.py Sunset https://www.timeanddate.com/sun/spain/sevilla '<tr><th>Sunset Today: </th><td>' '<span ' 'body' '/body' 86400",
 
 "python /var/www/html/Domo/backend/mqtt_send_to_topic_and_ddbb.py home/room/R ON"]

for cmd in cmd_list:
    subprocess.Popen(["lxterminal", "-e", cmd])
