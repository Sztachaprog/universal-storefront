from database import get_db_connection, close_db_connection

def execute_sql_file(file_path):
    # 1. Otwieramy połączenie używając TWOJEJ funkcji
    conn = get_db_connection()
    cursor = conn.cursor()


    # 2. Czytamy treść pliku (np. schema.sql) do zmiennej tekstowej
    # To jest tak, jakbyś skopiował tekst z Notatnika
    with open(file_path, 'r') as file:
        sql_script = file.read()
   
    # 3. Wykonujemy ten tekst jako komendę SQL
    cursor.execute(sql_script)

    # 4. Zatwierdzamy i zamykamy
    conn.commit()
    close_db_connection(conn, cursor)

    print(f"Wykonano skrypt: {file_path}")
        