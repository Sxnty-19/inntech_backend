import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("PGHOST"),
        dbname=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
        sslmode=os.getenv("PGSSLMODE")
    )

if __name__ == "__main__":
    try:
        print("Probando conexión...")
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT current_database(), current_user")
        print("Conexión exitosa:", cur.fetchone())
        conn.close()
    except psycopg2.Error as err:
        print("Conexión fallida:", err)