import uuid
from src.application import add_user
import psycopg2
from src.database import get_db_connection, close_db_connection




def test_create_user(db_connection):
    conn = db_connection
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM users;")
        conn.commit()
    except Exception as e:
        print(f"[ERROR] Database connection failed: {e}")

    


if __name__ == "__main__":
    test_create_user()
