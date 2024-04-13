
#python -m pip install mysql-connector-python

import mysql.connector
from mysql.connector import Error

ddbb_host = "localhost"
ddbb_user = "pi"
ddbb_password = "raspberry"
ddbb_database = "DomoServer"

# DDBB function to insert query parameter
def ddbb_insert_query(query):
    try: 
        mydb = mysql.connector.connect(
            host = ddbb_host,
            user = ddbb_user,
            password = ddbb_password,
            database = ddbb_database
        )

        mycursor = mydb.cursor()
        mycursor.execute(query)
        mydb.commit()

        mydb.close()
        print(mycursor.rowcount, "record(s) inserted")

    except mysql.connector.Error as err:
        print(f"DDBB insert error: {format(err)} ")
        mydb.close()
    

# DDBB function to select data following query command
def ddbb_select_query(query):
    try: 
        mydb = mysql.connector.connect(
            host = ddbb_host,
            user = ddbb_user,
            password = ddbb_password,
            database = ddbb_database
        )

        mycursor = mydb.cursor()
        mycursor.execute(query)

        mydb.close()
        return mycursor.fetchall()
    
    except mysql.connector.Error as err:
        print(f"DDBB select error: {format(err)} ")
        mydb.close()

# DDBB function to update parameters in database following query
def ddbb_update_query(query):
    try: 
        mydb = mysql.connector.connect(
            host = ddbb_host,
            user = ddbb_user,
            password = ddbb_password,
            database = ddbb_database
        )
        mycursor = mydb.cursor()
        mycursor.execute(query)
        mydb.commit()

        mydb.close()
        print(mycursor.rowcount, "record(s) updated")
    
    except mysql.connector.Error as err:
        print(f"DDBB update error: {format(err)} ")
        mydb.close()
