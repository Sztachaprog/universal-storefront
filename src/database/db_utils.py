from src.database.database import get_db_connection, close_db_connection

def execute_sql_file(file_path):
    conn = get_db_connection()
    cursor = conn.cursor()

    with open(file_path, 'r') as file:
        sql_script = file.read()
   
    cursor.execute(sql_script)

    conn.commit()
    close_db_connection(conn, cursor)

    print(f"Wykonano skrypt: {file_path}")
        