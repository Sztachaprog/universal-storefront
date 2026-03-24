from src.application import register_user
import pytest
import psycopg2

def test_create_user(cursor):
    register_user("bartek", "haslo", "bartek@example.com", is_premium=True)
    cursor.execute("SELECT username, password_hash, email, is_premium FROM users WHERE username = 'bartek';")
    user = cursor.fetchone()
    assert user is not None, "Użytkownik nie został znaleziony w bazie danych."
    assert user[0] == "bartek", f"Where looking for 'bartek', found '{user[0]}'"
    assert user[1] != "haslo", f"Different password than inputed '{user[1]}'"
    assert user[2] == "bartek@example.com", f"Where looking for 'bartek@example.com', found '{user[2]}'"
    assert user[3] == 1, f"Where looking for is_premium True, found {user[3]}"
    cursor.execute("SELECT username, email, is_premium FROM users WHERE username = 'bartek';")
    user = cursor.fetchone()
    print(f"Test completed successfully: {user}")
def test_duplicate_user(cursor):
        register_user("kacper", "password", "kacper@example.com")
        cursor.execute("SELECT username, password_hash, email, is_premium FROM users WHERE username = 'kacper';")
        with pytest.raises(psycopg2.errors.UniqueViolation):
             register_user("kacper", "password", "kacper@example.com", is_premium=True)

        