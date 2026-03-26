import bcrypt
from src.database.database import get_db_connection, close_db_connection

# CREATE
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


# GET
def get_user_by_name(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email, is_premium FROM users WHERE username = %s;", (username,))
    user = cursor.fetchone()
    close_db_connection(conn, cursor)
    return user
def get_user_by_mail(email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email, is_premium FROM users WHERE email = %s;", (email,))
    user = cursor.fetchone()
    close_db_connection(conn, cursor)
    return user
def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email, is_premium FROM users WHERE id = %s;", (user_id,))
    user = cursor.fetchone()
    close_db_connection(conn, cursor)
    return user
def get_user_password_hash(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM users WHERE id = %s;", (user_id,))
    password_hash = cursor.fetchone()
    close_db_connection(conn, cursor)
    return password_hash[0] if password_hash else None
# DELETE
def delete_user(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s;", (user_id,))
        conn.commit()
    except Exception as e:
        print(f"[ERROR] while deleting user: {e}")
        conn.rollback()
        raise e
    finally:
        close_db_connection(conn, cursor)   
# UPDATE
def update_user_profile(user_id, username, email, is_premium):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""UPDATE users
            SET username = %s,
            email = %s, 
            is_premium = %s
            WHERE id = %s;""", (username,email, is_premium, user_id))
        conn.commit()
    except Exception as e:
        print(f"[ERROR] while updating user: {e}")
        conn.rollback()
        raise e
    finally:
        close_db_connection(conn, cursor)   
def update_user_password(user_id, new_password):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        byte_password = new_password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(byte_password, salt).decode('utf-8')
        cursor.execute("UPDATE users SET password_hash = %s WHERE id = %s;", (hashed_password, user_id))
        conn.commit()
    except Exception as e:
        print(f"[ERROR] while updating user password: {e}")
        conn.rollback()
        raise e
    finally:
        close_db_connection(conn, cursor)

