from src.database.db_utils import execute_sql_file
import pytest
from src.database.database import get_db_connection, close_db_connection

@pytest.fixture(scope="session", autouse=True)
def CreateTestData():
    execute_sql_file("src/database/sql/schema.sql")
    execute_sql_file("src/database/sql/seed.sql")

@pytest.fixture(scope="function", autouse=True)
def cursor(): # Zmieniamy nazwę na bardziej logiczną
    conn = get_db_connection()
    cursor = conn.cursor() # Tworzymy kursor
    yield cursor # Dajemy testowi kursor, a nie całe połączenie!
    close_db_connection(conn, cursor) # Sprzątamy oba
@pytest.fixture(scope="function", autouse=True)
def clean_up():  
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("TRUNCATE TABLE users RESTART IDENTITY CASCADE;")
    conn.commit()

    yield

    close_db_connection(conn, cursor)
    

