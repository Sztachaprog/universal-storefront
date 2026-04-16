from src.database.db_utils import execute_sql_file
import pytest
from src.database.database import get_db_connection, close_db_connection

@pytest.fixture(scope="session", autouse=True)
def CreateTestData():
    execute_sql_file("src/database/sql/schema.sql")

@pytest.fixture(scope="function", autouse=True)
def cursor(): # Zmieniamy nazwę na bardziej logiczną
    conn = get_db_connection()
    cursor = conn.cursor() # Tworzymy kursor
    cursor.execute("TRUNCATE TABLE users, movies RESTART IDENTITY CASCADE;")
    conn.commit()

    yield cursor # Dajemy testowi kursor, a nie całe połączenie!

    cursor.execute("TRUNCATE TABLE users, movies, user_access, movie_access RESTART IDENTITY CASCADE;")
    conn.commit()
    close_db_connection(conn, cursor) # Sprzątamy oba


