import uuid
from src.application import add_user
import psycopg2
from src.database import get_db_connection, close_db_connection

def test_create_user():

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        user = add_user({uuid.uuid4()}, True)     
        conn.commit()


        
        return user
        # user_id = cursor.fetchone()[0]
        # cursor.execute("SELECT * FROM users WHERE id = %s", (user_id['id'],))
        # return user_id
    
    except Exception as e:
        print(f"[ERROR] Database connection failed: {e}")

    finally:
        close_db_connection(conn, cursor)
    


if __name__ == "__main__":
    test_create_user()
