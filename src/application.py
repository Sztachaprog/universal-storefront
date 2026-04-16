

from venv import logger

import bcrypt
from src.database.database import get_db_connection, close_db_connection

# CREATE users
def register_user(username, password, email, is_premium=False):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "INSERT INTO users (username, password_hash, email, is_premium) VALUES (%s, %s, %s, %s) RETURNING id;"
        byte_password = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(byte_password, salt).decode('utf-8')
        cursor.execute(query, ( username, hashed_password, email, is_premium))
        user_id = cursor.fetchone()[0]
        conn.commit()
        return user_id
    except Exception as e:
        print(f"[ERROR] while registering user: {e}")
        conn.rollback()
        raise e
    finally:
        close_db_connection(conn, cursor)   


# GET users
def get_user_by_name(username):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, email, is_premium FROM users WHERE username = %s;", (username,))
        user = cursor.fetchone()
        return user
    except Exception as e:
        print(f"[ERROR] while fetching user by name: {e}")
        raise e
    finally:
        close_db_connection(conn, cursor)
def get_user_by_mail(email):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, email, is_premium FROM users WHERE email = %s;", (email,))
        user = cursor.fetchone()
        return user
    except Exception as e:
        print(f"[ERROR] while fetching user by email: {e}")
        raise e
    finally:
        close_db_connection(conn, cursor)
def get_user_by_id(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, email, is_premium FROM users WHERE id = %s;", (user_id,))
        user = cursor.fetchone()
        return user
    except Exception as e:
        print(f"[ERROR] while fetching user by ID: {e}")
        raise e
    finally:
        close_db_connection(conn, cursor)
def get_user_password_hash(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash FROM users WHERE id = %s;", (user_id,))
        password_hash = cursor.fetchone()
        return password_hash[0] if password_hash else None
    except Exception as e:
        print(f"[ERROR] while fetching user password hash: {e}")
        raise e
    finally:
        close_db_connection(conn, cursor)
# DELETE users
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
# UPDATE users
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
def upgrade_user_to_premium(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET is_premium = TRUE where id = %s;", (user_id,))
        conn.commit()
    except Exception as e:
        print(f"[ERROR] while upgrading user to premium: {e}")
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


# CREATE movies
def create_movie(release_date, is_premium_only, language_code, title, description):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query_movie = "INSERT INTO movies (release_date, is_premium_only) VALUES (%s, %s) RETURNING id;"
        cursor.execute(query_movie, (release_date, is_premium_only))
        movie_id = cursor.fetchone()[0]
        query_movie_language = "INSERT INTO movie_translations (movie_id, language_code, title, description) VALUES (%s, %s, %s, %s);"
        cursor.execute(query_movie_language, (movie_id, language_code, title, description))
        conn.commit()
        return movie_id
    except Exception as e:
        print(f"[ERROR] while creating movie: {e}")
        conn.rollback()
        raise e
    finally:
        close_db_connection(conn, cursor)
# GET movies
def get_movie_details(movie_id, language_code):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT movies.id, movies.release_date, movies.is_premium_only, movie_translations.title, movie_translations.description
            FROM movies 
            JOIN movie_translations ON movies.id = movie_translations.movie_id
            WHERE movies.id = %s AND movie_translations.language_code = %s;
        """, (movie_id, language_code))
        movie = cursor.fetchone()
        return movie
    except Exception as e:
        print(f"[ERROR] while fetching movie details: {e}")
        raise e
    finally:
        close_db_connection(conn, cursor)
# UPDATE movies
def update_movie(release_date, is_premium_only, language_code, title, description, movie_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE movies
            SET release_date = %s,
            is_premium_only = %s 
            WHERE id = %s;
        """, (release_date, is_premium_only, movie_id))
        cursor.execute("""
            UPDATE movie_translations
            SET language_code = %s,
            title = %s,
            description = %s
            WHERE movie_id = %s; 
        """, (language_code, title, description, movie_id))
        conn.commit()
        return movie_id
    except Exception as e:
        print(f"[ERROR] while fetching movie details: {e}")
        raise e
    finally:
        close_db_connection(conn, cursor)
def delete_movie(move_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM movies WHERE id = %s;", (move_id,))
        conn.commit()
    except Exception as e:
        print(f"[ERROR] while deleting user: {e}")
        conn.rollback()
        raise e
    finally:
        close_db_connection(conn, cursor)   


# Access control
def grant_ppv_access(user_id, movie_id, cursor):
    try:
        cursor.execute("SELECT is_premium FROM users WHERE id = %s;", (user_id,))
        is_user_premium = cursor.fetchone()[0]

        if is_user_premium:
            return False, "User already has premium access"
        if user_id is None or movie_id is None:
            return False, "Invalid user ID or movie ID"


        # New ppv access for user 
        cursor.execute("INSERT INTO user_access (user_id, movie_id) VALUES user_id = %s, movie_id = %s RETURNING id; "(user_id, movie_id))
        new_ppv = cursor.fetchone()[0]

        
        cursor.commit()
        return True, "PPV access granted"


    except:
        logger.error(f"Error granting PPV access for user_id: {user_id}, movie_id: {movie_id}")
        cursor.rollback()
        return False, "Error granting PPV access"

    finally:
        close_db_connection(conn, cursor)
    

def process_watch_request(user_id, movie_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if user is premium
        cursor.execute("SELECT is_premium FROM users WHERE id = %s;", (user_id,))
        is_user_premium = cursor.fetchone()[0]

        #check if movie is premium only
        cursor.execute("SELECT is_premium_only FROM movies WHERE id = %s;", (movie_id,))
        is_movie_premium_only = cursor.fetchone()[0]

        # Check if user have ppv access
        cursor.execute("SELECT user_id, movie_id, expires_at FROM user_access " \
        "WHERE user_id = %s AND movie_id = %s AND expires_at > NOW();", (user_id, movie_id,))
        result = cursor.fetchone()
        has_ppv_access = result is not None

        return(
            is_user_premium
            or not is_movie_premium_only
            or has_ppv_access
        )
    except Exception as e:
        print(f"[ERROR] while processing watch request: {e}")
        raise e
    finally:
        close_db_connection(conn, cursor)