import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

if __name__ == "__main__":
    print("=== PRUEBA ===\n")
    try:
        conn = get_db_connection()
        if conn.is_connected():
            print("Conexión exitosa a la base de datos:", os.getenv("DB_NAME"))
        conn.close()
    except mysql.connector.Error as err:
        print("ERROR de conexión:", err)