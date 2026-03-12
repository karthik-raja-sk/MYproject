
import psycopg2
import os
from dotenv import load_dotenv

# Load .env from the same directory or parent
dotenv_path = ".env"
if not os.path.exists(dotenv_path):
    dotenv_path = "../.env"

load_dotenv(dotenv_path)

db_url = os.getenv("DATABASE_URL")
print(f"Testing connection to: {db_url}")

if not db_url:
    print("Error: DATABASE_URL not found in .env")
    exit(1)

try:
    conn = psycopg2.connect(db_url)
    print("Connection successful!")
    
    # Check if database exists by querying pg_database
    cur = conn.cursor()
    cur.execute("SELECT current_database();")
    db_name = cur.fetchone()[0]
    print(f"Connected to database: {db_name}")
    
    cur.close()
    conn.close()
except psycopg2.OperationalError as e:
    if "database \"resume_matcher\" does not exist" in str(e):
        print("Error: Database 'resume_matcher' does not exist. Please create it.")
    else:
        print(f"Connection failed (OperationalError): {e}")
except Exception as e:
    print(f"Connection failed: {e}")
