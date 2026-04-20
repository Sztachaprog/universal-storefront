from src.application import (
    register_user, 
    get_user_by_name, 
    get_user_by_mail, 
    get_user_by_id,
    delete_user,
    update_user_profile,
    update_user_password,
    get_user_password_hash,
    upgrade_user_to_premium
)
import pytest
import psycopg2

#Create
def test_create_user(cursor):
    register_user("bartek", "haslo", "bartek@example.com", is_premium=True, cursor=cursor)
    cursor.execute("SELECT username, password_hash, email, is_premium FROM users WHERE username = 'bartek';")
    user = cursor.fetchone()
    assert user is not None, "User not found in database."
    assert user[0] == "bartek", f"Where looking for 'bartek', found '{user[0]}'"
    assert user[1] != "haslo", f"Different password than inputed '{user[1]}'"
    assert user[2] == "bartek@example.com", f"Where looking for 'bartek@example.com', found '{user[2]}'"
    assert user[3] == True, f"Where looking for is_premium True, found {user[3]}"
    cursor.execute("SELECT username, email, is_premium FROM users WHERE username = 'bartek';")
    user = cursor.fetchone()
    print(f"Test completed successfully: {user}")
def test_duplicate_user(cursor):
        register_user("kacper", "password", "kacper@example.com")
        cursor.execute("SELECT username, password_hash, email, is_premium FROM users WHERE username = 'kacper';")
        with pytest.raises(psycopg2.errors.UniqueViolation):
             register_user("kacper", "password", "kacper@example.com", is_premium=True)
# Read
def test_get_user_by_name():
    register_user("user", "password123", "mail@mail.com")
    user = get_user_by_name("user")
    assert user is not None, "User not found in database"
    assert user[1] == "user", f"Expected username 'user', got '{user[1]}'"
    assert user[2] == "mail@mail.com", f"Expected email 'mail@mail.com', got '{user[2]}'"
    assert user[3] == False, f"Expected is_premium False, got {user[3]}"
def test_get_user_by_mail():
    register_user("user", "password123", "mail@mail.com")
    user = get_user_by_mail("mail@mail.com")
    assert user is not None, "User not found in database"
    assert user[1] == "user", f"Expected username 'user', got '{user[1]}'"
    assert user[2] == "mail@mail.com", f"Expected email 'mail@mail.com', got '{user[2]}'"
    assert user[3] == False, f"Expected is_premium False, got {user[3]}"
def test_get_user_by_id():
    registered = register_user("user", "password123", "mail@mail.com")
    user = get_user_by_id(registered)
    assert user is not None, "User not found in database"
    assert user[0] == registered, f"Expected user ID {registered}, got '{user[0]}'"
    assert user[1] == "user", f"Expected username 'user', got '{user[1]}'"
    assert user[2] == "mail@mail.com", f"Expected email 'mail@mail.com', got '{user[2]}'"
    assert user[3] == False, f"Expected is_premium False, got {user[3]}"
# Delete
def test_delete_user(cursor):
    register_user("user", "password123", "mail@mail.com")
    delete_user(1)
    cursor.execute("SELECT * FROM users WHERE id = 1;")
    user = cursor.fetchone()
    assert user is None, "User not deleted from database"
# Update
def test_update_user():
    register_user("user", "password123", "mail@mail.com", is_premium=True)
    update_user_profile(1, "userr", "maill@mail.com", is_premium=False)
    user = get_user_by_id(1)
    assert user[1] == "userr", f"Expected updated username = userr, got '{user[1]}'"
def test_update_user_password():
    register_user("user", "password123", "mail@mail.com")
    old_password = get_user_password_hash(1)
    update_user_password(1, "newpassword")
    new_password = get_user_password_hash(1)
    assert old_password != new_password, "Password hash should be different after updated"
def test_upgrade_user_to_premium():
    non_premium_user = register_user("user", "password123", "mail@mail.com")
    upgrade_user_to_premium(non_premium_user)
    premium_user = get_user_by_id(non_premium_user)

    assert premium_user[3] == True, "User not upgraded to premium"
