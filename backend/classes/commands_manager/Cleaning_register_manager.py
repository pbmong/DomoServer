import os

from libraries import database_access as ddbb

class Cleaning_register_manager:
    
    # ID´s dictiorary
    min_ids_dict = {
        "home/bedroom/R OFF": 0,
        "home/bedroom/R ON": 10,
        "home/bedroom/L OFF": 20,
        "home/bedroom/L ON": 30,
        "home/bedroom/C OFF": 40,
        "home/bedroom/C ON": 50
        }

    max_ids_dict = {
        "home/bedroom/R OFF": 9,
        "home/bedroom/R ON": 19,
        "home/bedroom/L OFF": 29,
        "home/bedroom/L ON": 39,
        "home/bedroom/C OFF": 49,
        "home/bedroom/C ON": 59
      }
    
    def __init__(self):
        pass

    def insert_register(self, datetime, room, level):

        try:
            # Get last id for command
            query = F"SELECT * FROM cleaning_register ORDER BY `ID` DESC"
            result = ddbb.ddbb_select_query(query)
            
            # Check if there is an id available
            if len(result) > 0:
                id = result[0][0] + 1
                
            else:
                id = 1

            # Insert command into database
            query = F"INSERT INTO cleaning_register (ID, DATETIME, ROOM, LEVEL) VALUES ({id}, '{datetime}', '{room}', '{level}')"
            
            result = ddbb.ddbb_insert_query(query)
        
        except Exception as e:
            result = F"Error: {e}"

        return result

    # Delete command from database
    def delete_register(self, id):
        
        query = F"DELETE FROM cleaning_register WHERE ID = '{id}'"
        result = ddbb.ddbb_delete_query(query)
        return result
