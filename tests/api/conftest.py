import pytest
from src.database.database import get_db_connection, close_db_connection

BASE_URL = "http://localhost:5000/api"

@pytest.fixture(scope="function", autouse=False)
def conn():
    conn = get_db_connection()
    yield conn
    close_db_connection(conn)

@pytest.fixture(scope="function", autouse=True)
def cursor(conn):
    cursor = conn.cursor()

    yield cursor

    cursor.execute("TRUNCATE TABLE users, movies, user_access RESTART IDENTITY CASCADE;")
    conn.commit()
    close_db_connection(conn)

