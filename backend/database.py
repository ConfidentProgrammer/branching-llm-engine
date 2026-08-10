from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
load_dotenv()
# Get values from environment variables
USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")

# Connection string format: postgresql://user:password@localhost:5432/dbname
DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@localhost:5432/{DB_NAME}"

# 1. Create Engine: The gateway to the database
engine = create_engine(DATABASE_URL)

# 2. SessionLocal: A factory for creating database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Base: A class that all our models will inherit from
Base = declarative_base()

# Dependency: Used in FastAPI routes to get a DB session and close it after the request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()