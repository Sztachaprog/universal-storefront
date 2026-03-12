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
            ('Bartsek', TRUE)
            RETURNING id;
        """)    

        new_user_id = cursor.fetchone()[0]
        conn.commit()
        
        cursor.execute("SELECT id, username, is_premium FROM users WHERE id = %s;", (new_user_id,))
        extracted_user = cursor.fetchone()

        # 3. Asercja - sprawdzamy czy imię się zgadza
        assert extracted_user[1] == 'Bartsek', f"Błąd! Oczekiwano Bartsek, a jest {extracted_user[1]}"
        
        print(f"[DATA] Extracted user details: ID={extracted_user[0]}, Name={extracted_user[1]}")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"[ERROR] Database connection failed: {e}")
    
if __name__ == "__main__":
    test_db_connection()
