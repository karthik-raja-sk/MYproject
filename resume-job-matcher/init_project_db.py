from sqlalchemy import create_engine, text
import os
import sys

# Standard connection strings
BASE_URL = "postgresql://postgres:12345678@localhost:5432/postgres"
APP_DB_URL = "postgresql://postgres:12345678@localhost:5432/resume_matcher"
DB_NAME = "resume_matcher"

def ensure_db_exists():
    print(f"Checking if database '{DB_NAME}' exists...")
    try:
        engine = create_engine(BASE_URL, isolation_level='AUTOCOMMIT')
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname='{DB_NAME}'"))
            if not result.fetchone():
                print(f"Creating database '{DB_NAME}'...")
                conn.execute(text(f"CREATE DATABASE {DB_NAME}"))
                print("Database created.")
            else:
                print(f"Database '{DB_NAME}' already exists.")
    except Exception as e:
        print(f"Error checking/creating database: {e}")
        # Don't exit here, maybe it exists but we couldn't check

def init_tables():
    print("Initializing database tables...")
    # Add backend to path to import app models
    backend_path = os.path.join(os.getcwd(), 'backend')
    if backend_path not in sys.path:
        sys.path.append(backend_path)
    
    try:
        from app.database import Base, engine
        # This will create all tables defined in models.py
        from app import models 
        Base.metadata.create_all(bind=engine)
        print("Database tables initialized successfully.")
    except Exception as e:
        print(f"Error initializing tables: {e}")
        sys.exit(1)

if __name__ == "__main__":
    ensure_db_exists()
    init_tables()
