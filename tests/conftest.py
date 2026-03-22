import pytest
from database.database import get_db_connection, close_db_connection

@pytest.fixture(scope="module")
def db_connection():
    conn = get_db_connection() # Próba nawiązania połączenia z bazą danych
    if not conn: 
        pytest.skip("Nie można nawiązać połączenia z bazą danych.") 
    yield conn # Testy będą korzystać z tego połączenia
    close_db_connection(conn, None) # Zamykamy połączenie po zakończeniu testów

