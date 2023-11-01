import os
import sys
import shutil

folder_destiny = "/var/www/html/Domo/files/home_bedroom_2023-10-08_10-55-02/"
files_download_folder = folder_destiny
files_list = os.listdir(files_download_folder)

entries = ""
for entry in files_list:
    entries += " " + folder_destiny + entry

os.system("python /var/www/html/Domo/backend/send_email.py 'Domotic Raspbian Service detecte and intruder' " + entries)

#print("python /var/www/html/Domo/backend/send_email.py 'Domotic Raspbian Service detecte and intruder' " + entries)