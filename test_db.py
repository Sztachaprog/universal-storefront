import psycopg2

def test_db_connection():
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
        print("\n[CONFIRMED] Database connection successful!")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) NOT NULL,
            is_premium BOOLEAN NOT NULL DEFAULT FALSE
            );
        """)

        cursor.execute("""
            INSERT INTO users (username, is_premium) VALUES
            ('Bartek', TRUE)
        """)    

        conn.commit()
        cursor.execute("SELECT * FROM users")
        user = cursor.fetchone()
        print("[CONFIRMED] Database operations successful!")
        print(f"Retrieved user: {user}")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"[ERROR] Database connection failed: {e}")
    
if __name__ == "__main__":
    test_db_connection()
