import psycopg2

def test_database_connection():
    # 1. Konfiguracja połączenia (dane z Twojego docker-compose.yml)
    connection_params = {
        "host": "localhost",
        "port": "5432",
        "database": "storefront",
        "user": "user",
        "password": "password"
    }

    try:
        # 2. Nawiązanie połączenia
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()
        print("\n[SUCCESS] Connected to PostgreSQL!")

        # 3. Tworzenie tabeli (jeśli nie istnieje)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username TEXT NOT NULL,
                is_premium BOOLEAN DEFAULT FALSE
            );
        """)
        
        # 4. Dodanie testowego użytkownika
        cursor.execute("INSERT INTO users (username, is_premium) VALUES ('Bartek_VOD', True);")
        conn.commit()
        print("[SUCCESS] Table created and user added!")

        # 5. Sprawdzenie, czy użytkownik tam jest
        cursor.execute("SELECT * FROM users;")
        user = cursor.fetchone()
        print(f"[DATA] Found user: {user}")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"[ERROR] Connection failed: {e}")

if __name__ == "__main__":
    test_database_connection()