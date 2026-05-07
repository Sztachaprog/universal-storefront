from src.database.db_utils import execute_sql_file
import pytest
from src.database.database import get_db_connection, close_db_connection

@pytest.fixture(scope="function", autouse=True)
def cursor(): 
    conn = get_db_connection()
    cursor = conn.cursor() 

    yield cursor 

    conn.rollback() 
    close_db_connection(conn, cursor) 


