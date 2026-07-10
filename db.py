import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            ssl_ca="ca.pem",
            ssl_verify_cert=True,
            connection_timeout=10,
            autocommit=True
        )

        print("✅ Database Connected")
        return connection

    except Error as e:
        print("❌ Database Error:", e)
        raise