import os
import threading
from subprocess import Popen, PIPE, CalledProcessError

# Services list to be executed in backend
executable_files = [
        [[],["python weather_api_consult.py"]],
        [[],["python ddbb_programed_commands.py"]],
        [[],["python mqtt_listener_to_ddbb.py"]],
    ]

# Function to run the script
def run_script(script_execution_cmd):
    os.system(script_execution_cmd) #TODO: Print each thread output with thread identifi
    print("Script finished: ", script_execution_cmd)

# Execute all scripts in parallel
for program in executable_files:
    print("Executing: ", program[1])
    program[0] = threading.Thread(target=run_script, args=(program[1]))
    program[0].start()

for program in executable_files:
    program[0].join()

print("Scripts launched successfully.")