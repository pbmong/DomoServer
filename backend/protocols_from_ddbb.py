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


print("Executing programmed protocols")
while True:
    try:
        # Select programmed commands from database
        protocols_list = ddbb.ddbb_select_query("SELECT * FROM protocols")
        
        for protocol in protocols_list:
            curr_dt = datetime.datetime.now()
            curr_time =  datetime.time(hour=int(curr_dt.hour), minute=int(curr_dt.minute))
            week_dy = datetime.datetime.today().weekday() + 1
            
            prt_topics_list = protocol[1].split(' ')
            prt_start_dt = datetime.time(hour=int(protocol[2][11:13]), minute=int(protocol[2][14:16]))
            prt_stop_dt = datetime.time(hour=int(protocol[3][11:13]), minute=int(protocol[2][14:16]))
            prt_weekday = protocol[4]
            prt_min_val = protocol[5]
            prt_max_val = protocol[6]
            prt_state = protocol[7]
            
            if prt_state:
            
                # Check if the programmed command is for the current day
                if check_weekday(week_dy, prt_weekday):
                    
                    # If current time is in datetime range
                    if (prt_start_dt <= curr_time) and (curr_time <= prt_stop_dt):
                        
                        # Get current supervised parameter state
                        indexes = [x for x, v in enumerate(prt_topics_list[0]) if v == '/']
                        ddbb_table = prt_topics_list[0][0:indexes[len(indexes)-1]]
                        ddbb_table = ddbb_table.replace('/','_')
                        ddbb_meaning = prt_topics_list[0][indexes[len(indexes)-1]+1:len(prt_topics_list[0])]
                        
                        supervised_parameter_data = ddbb.ddbb_select_query(f"SELECT VALUE FROM {ddbb_table} WHERE MEANING = '{ddbb_meaning}' ")[0][0]
                        
                        # Get current control parameter state
                        indexes = [x for x, v in enumerate(prt_topics_list[1]) if v == '/']
                        ddbb_table = prt_topics_list[1][0:indexes[len(indexes)-1]]
                        ddbb_table = ddbb_table.replace('/','_')
                        ddbb_meaning = prt_topics_list[1][indexes[len(indexes)-1]+1:len(prt_topics_list[1])]
                        
                        control_parameter_data = ddbb.ddbb_select_query(f"SELECT VALUE FROM {ddbb_table} WHERE MEANING = '{ddbb_meaning}' ")[0][0]
                        
                        # Check lower histeresis
                        if (int(supervised_parameter_data) < int(prt_min_val)) and (control_parameter_data == 'OFF'):
                            # Start control
                            res = os.system(f"python mqtt_send_to_topic_and_ddbb.py {prt_topics_list[1]} ON 2")

                        # Check upper histeresis
                        if (int(supervised_parameter_data) > int(prt_max_val)) and (control_parameter_data == 'ON'):
                            # Stop control
                            res = os.system(f"python mqtt_send_to_topic_and_ddbb.py {prt_topics_list[1]} OFF 2")
                        
                                                                    
    except Exception as e:
        print(f"Exception processing programmed protocols: {e}")
    
    time.sleep(waiting_delay)