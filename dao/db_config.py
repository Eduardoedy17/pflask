import sqlite3

#path / url de conexão
DB_PATH = 'banco_escola.db'
    
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn
