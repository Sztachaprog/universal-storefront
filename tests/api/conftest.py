import pytest
import jwt
from src.database.database import get_db_connection, close_db_connection
from datetime import datetime, timezone, timedelta

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

@pytest.fixture(scope="function", autouse=False)
def create_token():              
    def _make(user_id):        
        return jwt.encode(
            {"user_id": user_id, "exp": datetime.now(timezone.utc) + timedelta(minutes=15)},
            "dev-secret-key",
            "HS256"
        )
    return _make              
