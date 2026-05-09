from src.database.db_utils import execute_sql_file
import pytest

@pytest.fixture(scope="session", autouse=True)
def CreateTestData():
    execute_sql_file("src/database/sql/schema.sql")