
from src.database import get_db_connection, close_db_connection

def add_user(username, is_premium=False):
    """Dodaje użytkownika do bazy i zwraca jego ID."""
    conn = get_db_connection()
    if not conn:
        return None
        
    cursor = conn.cursor()
    try:
        query = "INSERT INTO users (username, is_premium) VALUES (%s, %s) RETURNING id;"
        cursor.execute(query, (username, is_premium))
        user_id = cursor.fetchone()[0]
        conn.commit()
        return user_id
    except Exception as e:
        print(f"[ERROR] Błąd podczas dodawania użytkownika: {e}")
        conn.rollback()
        return None
    finally:
        close_db_connection(conn, cursor)

def get_user_by_id(user_id):
    """Pobiera dane użytkownika o konkretnym ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, is_premium FROM users WHERE id = %s;", (user_id,))
    user = cursor.fetchone()
    close_db_connection(conn, cursor)
    return user