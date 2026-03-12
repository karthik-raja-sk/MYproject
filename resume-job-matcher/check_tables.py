
import psycopg2
import os
from dotenv import load_dotenv

# Load .env from the same directory or parent
dotenv_path = ".env"
if not os.path.exists(dotenv_path):
    dotenv_path = "../.env"

load_dotenv(dotenv_path)

db_url = os.getenv("DATABASE_URL")

try:
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
    """)
    tables = cur.fetchall()
    print("Tables in database:")
    for table in tables:
        print(f" - {table[0]}")
    
    if not tables:
        print("No tables found. Database might need initialization.")
    
    cur.close()
    conn.close()
except Exception as e:
    print(f"Error: {e}")
