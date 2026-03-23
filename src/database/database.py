import psycopg2
from psycopg2 import OperationalError

connection_params = {
    "host":"localhost",
    "port": "5433",
    "database":"storefront",
    "user":"user",    
    "password":"password"
}

def get_db_connection():
    try:
        conn = psycopg2.connect(**connection_params)
        return conn
    except OperationalError as e:
        print(f"[ERROR] Database connection failed: {e}")
        raise e
def close_db_connection(conn, cursor=None):
    if cursor:
        cursor.close()
    if conn:
        conn.close()