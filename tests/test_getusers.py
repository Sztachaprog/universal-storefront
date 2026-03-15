import psycopg2

def test_get_user():
    connection_params = {
        "host": "localhost",
        "port": "5433",
        "database": "storefront",
        "user": "user",
        "password": "password"
    }

    try:
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()

        cursor.execute("""
        SELECT id, username, is_premium 
        FROM users;
    """)
        users = cursor.fetchall()
        assert len(users) > 0, "No users found in the database!"
        print(f"\n Users: {users}")


        cursor.close()
        conn.close()

    except Exception as e:
        print(f"[ERROR] Failed to retrieve user: {e}")

if __name__ == "__main__":
    test_get_user()