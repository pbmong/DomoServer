import os

from classes.commands_manager.Cleaning_register_manager import Cleaning_register_manager

operations_list = ["Insert", "Delete"]

# Get command operation
operation = os.sys.argv[1]

# Execute supported operation

match operation:
    case "Insert":
        # Get operation parameters
        datetime = os.sys.argv[2]
        room = os.sys.argv[3]
        level = os.sys.argv[4]

        result = Cleaning_register_manager().insert_register(datetime, room, level)
        print(result)

    case "Delete":
        # Get operation parameters
        command_id = os.sys.argv[2]

        result = Cleaning_register_manager().delete_register(command_id)
        print(result)
    case _:
        print("Operation not supported")

