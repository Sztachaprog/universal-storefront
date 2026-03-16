import psycopg2
from src.application import add_user, get_user_by_id

def test_add_and_retrieve_user():    
    try:

        add_user("Bartsek", True)

        get_user_by_id(1)  


    except Exception as e:
        print(f"[ERROR] Database connection failed: {e}")
    

def test_delete_created_user():
    connection_params = {
        "host":"localhost",
        "port": "5433",
        "database":"storefront",
        "user":"user",    
        "password":"password"
    }
    try:
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM users
            WHERE id NOT IN (
                SELECT MIN(id)
                FROM users
                GROUP BY username
            );
        """)
        conn.commit()


    except Exception as e:
        print(f"[ERROR] Database connection failed: {e}")
        
    
if __name__ == "__main__":
    test_add_and_retrieve_user()
    test_delete_created_user()
