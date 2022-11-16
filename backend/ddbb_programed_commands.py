import sys
import os
import mysql.connector
from mysql.connector import Error
import time
import datetime

def ddbb_send_query(query):
    try: 
        mydb = mysql.connector.connect(
        host = "localhost",
        user = "pi",
        password = "raspberry",
        database = "DomoServer"
        )

        mycursor = mydb.cursor()
        mycursor.execute(query)

        return mycursor.fetchall()
    except:
        print(f"DDBB error: {Error} ")

def check_weekday(week_dy, programed_dy_bin):

    if week_dy == 1:
         week_dy_bin = 1
    elif week_dy == 2:
         week_dy_bin = 2
    elif week_dy == 3:
         week_dy_bin = 4
    elif week_dy == 4:
         week_dy_bin = 8
    elif week_dy == 5:
         week_dy_bin = 16
    elif week_dy == 6:
         week_dy_bin = 32
    elif week_dy == 7:
         week_dy_bin = 64

    res = bin(week_dy_bin & programed_dy_bin)
    #print(f"week_dy: {week_dy} | programed_dy: {programed_dy_bin} | res {int(res, 2)}")

    return int(res, 2)

def check_datetime(curr_dt , programed_dt):
    
    try:
        check = True
        #print(f"checking time | Current: {curr_dt} , Programmed: {programed_dt}")
        
        if programed_dt[0:4] != '****':
            if(curr_dt.year != int(programed_dt[0:4],10)):
                check = False
        if check == False:
            return check
        
        if programed_dt[5:7] != '**':
            if(curr_dt.month != int(programed_dt[5:7],10)):
                check = False
        if check == False:
            return check
        
        if programed_dt[8:10] != '**':
            if(curr_dt.day != int(programed_dt[8:10],10)):
                check = False
        if check == False:
            return check

        if programed_dt[11:13] != '**':
            if(curr_dt.hour != int(programed_dt[11:13],10)):
                check = False
        if check == False:
            return check

        if programed_dt[14:16] != '**':
            if(curr_dt.minute != int(programed_dt[14:16],10)):
                check = False
        if check == False:
            return check

        #if programed_dt[17:19] != '**':
        #    if(curr_dt.minute != int(programed_dt[17:19],10)):
        #        check = False

        return check
    except:
        print(f"Exception processing datetime: {programed_dt}")
        return False;


while True:
    for x in ddbb_send_query("SELECT * FROM programed_commands"):
        curr_dt = datetime.datetime.now()
        week_dy = datetime.datetime.today().weekday() + 1
        if check_weekday(week_dy, x[3]) and check_datetime(curr_dt , x[2]):
                print(f"->({curr_dt}) {x[2]}: {x[1]}")
                res = os.system(x[1])
                print(res)   
                print("-------------------------------------------------------------")                                                 
    
    time.sleep(60)