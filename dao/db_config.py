import sqlite3
import psycopg2

#path / url de conexão
DB_PATH = 'postgresql://neondb_owner:npg_WIxGylq80cOg@ep-red-queen-ac9w25m0-pooler.sa-east-1.aws.neon.tech/neondb?sslmode=require'
    
def get_db_connection():
    conn = psycopg2.connect(DB_PATH)
    return conn
