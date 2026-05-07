from src.database.db_utils import execute_sql_file
import pytest
from src.database.database import get_db_connection, close_db_connection


@pytest.fixture(scope="function", autouse=True)
def cursor(): 
    


