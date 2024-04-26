import sys
import os
import time
import datetime

from libraries import database_access as ddbb

waiting_delay = 60

# Function to check if the programmed day is the same as the current day
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

    return int(res, 2)

# Function to check if the programmed time is the same as the current time
def check_datetime(curr_dt , programed_dt):
    
    try:
        check = True
        # Year checking
        if programed_dt[0:4] != '****':
            if(curr_dt.year != int(programed_dt[0:4],10)):
                check = False
        if check == False:
            return check
        
        # Month checking
        if programed_dt[5:7] != '**':
            if(curr_dt.month != int(programed_dt[5:7],10)):
                check = False
        if check == False:
            return check
        
        # Day checking
        if programed_dt[8:10] != '**':
            if(curr_dt.day != int(programed_dt[8:10],10)):
                check = False
        if check == False:
            return check

        # Hour checking
        if programed_dt[11:13] != '**':
            if(curr_dt.hour != int(programed_dt[11:13],10)):
                check = False
        if check == False:
            return check

        # Minute checking
        if programed_dt[14:16] != '**':
            if(curr_dt.minute != int(programed_dt[14:16],10)):
                check = False
        if check == False:
            return check

        return check
    except:
        print(f"Exception processing datetime: {programed_dt}")
        return False;


print("Executing programmed commands")
while True:
    try:
        # Select programmed commands from database
        command_list = ddbb.ddbb_select_query("SELECT * FROM programed_commands")
        
        for x in command_list:
            curr_dt = datetime.datetime.now()
            week_dy = datetime.datetime.today().weekday() + 1

            # Check if the programmed command is for the current day and time
            if check_weekday(week_dy, x[3]) and check_datetime(curr_dt , x[2]):
                    print(f"->({curr_dt}) {x[2]}: {x[1]}")
                    res = os.system(x[1])
                    print(res)   
                    print("-------------------------------------------------------------")                                                 
    except:
        print("Exception processing programmed commands")
    
    time.sleep(waiting_delay)
