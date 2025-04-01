import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def connect_to_db():

    try:
        conn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"), # Get database details from environment variables
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE")
        )
        print("Database connection established successfully.")
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None

def close_db_connection(conn):

    if conn:
        try:
            conn.close()
            print("Database connection closed.")
        except mysql.connector.Error as err:
            print(f"Error closing database connection: {err}")
        except Exception as e:
            print(f"Error during database connection close: {e}")

