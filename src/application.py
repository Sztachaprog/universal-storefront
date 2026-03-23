import bcrypt
from src.database.database import get_db_connection, close_db_connection


def register_user(username, password, email, is_premium=False):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "INSERT INTO users (username, password_hash, email, is_premium) VALUES (%s, %s, %s, %s) RETURNING id;"
        byte_password = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(byte_password, salt).decode('utf-8')
        cursor.execute(query, (username, hashed_password, email, is_premium))
        user_id = cursor.fetchone()[0]
        conn.commit()
        return user_id
    except Exception as e:
        print(f"[ERROR] while registering user: {e}")
        conn.rollback()
        raise e
    finally:
        close_db_connection(conn, cursor)

def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email, is_premium FROM users WHERE id = %s;", (user_id,))
    user = cursor.fetchone()
    close_db_connection(conn, cursor)
    return user