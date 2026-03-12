from sqlalchemy import create_engine, text
import os
import sys

# Standard connection strings
APP_DB_URL = "postgresql://postgres:12345678@localhost:5432/resume_matcher"

def reset_database():
    print("Resetting database schema...")
    # Add backend to path to import app models
    backend_path = os.path.join(os.getcwd(), 'backend')
    if backend_path not in sys.path:
        sys.path.append(backend_path)
    
    try:
        from app.database import Base, engine
        # Import models to ensure they are registered with Base
        from app import models 
        
        print("Dropping all existing tables...")
        Base.metadata.drop_all(bind=engine)
        
        print("Creating all tables with current schema...")
        Base.metadata.create_all(bind=engine)
        
        print("Database schema reset successfully.")
    except Exception as e:
        print(f"Error resetting database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    reset_database()
