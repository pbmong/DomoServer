import os

from classes.commands_manager.Commands_manager import Commands_manager

operations_list = ["Insert", "Delete"]

# Get command operation
operation = os.sys.argv[1]

# Execute supported operation

match operation:
    case "Insert":
        # Get operation parameters
        command = os.sys.argv[2]
        datetime = os.sys.argv[3]
        weekday = os.sys.argv[4]

        result = Commands_manager().insert_command(command, datetime, weekday)
        print(result)

    case "Delete":
        # Get operation parameters
        command_id = os.sys.argv[2]

        result = Commands_manager().delete_command(command_id)
        print(result)
    case _:
        print("Operation not supported")

