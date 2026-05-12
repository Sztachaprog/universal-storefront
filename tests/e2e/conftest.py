import pytest
from src.application import register_user
from src.database.database import get_db_connection, close_db_connection
from dataclasses import dataclass

@dataclass
class TestUser:
    username: str
    password: str
    email: str



@pytest.fixture(scope="function", autouse=False)
def conn():
    conn = get_db_connection()
    yield conn

@pytest.fixture(scope="function", autouse=True)
def cursor(conn):
    cursor = conn.cursor()

    yield cursor

    cursor.execute("TRUNCATE TABLE users, movies, user_access RESTART IDENTITY CASCADE;")
    conn.commit()
    close_db_connection(conn)

@pytest.fixture(scope="function", autouse=False)
def registered_user(cursor, conn):
    user = TestUser(
        username="testusername", 
        password="testpassword", 
        email="testuser@mail.com"
    )
    register_user(user.username, user.password, user.email, is_premium = False, cursor=cursor)
    conn.commit()
    return user
