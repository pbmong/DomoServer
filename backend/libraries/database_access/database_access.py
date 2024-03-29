
import mysql.connector
from mysql.connector import Error

def ddbb_insert_query(query):
    try: 
        mydb = mysql.connector.connect(
        host = "localhost",
        user = "pi",
        password = "raspberry",
        database = "DomoServer"
        )

        mycursor = mydb.cursor()
        mycursor.execute(query)
        mydb.commit()
        # print(mycursor.rowcount, "record(s) affected")

    except:
        print(f"DDBB error: {Error} ")

def ddbb_select_query(query):
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
        
def ddbb_update_query(query):
    try: 
        mydb = mysql.connector.connect(
        host = "localhost",
        user = "pi",
        password = "raspberry",
        database = "DomoServer"
        )
        mycursor = mydb.cursor()
        mycursor.execute(query)
        mydb.commit()
        print(mycursor.rowcount, "record(s) affected")
    except:
        print(f"DDBB error: {Error} ")