import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='your_password',
            database='cricbuzz_live_stats'
        )
        if connection.is_connected():
            print("connection establish mysql")
            return connection
    except Error as e:
        print(f"Error while connecting to database: {e}")
        return None
