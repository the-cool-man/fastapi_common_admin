# app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Replace with your actual Postgres credentials
DATABASE_URL = "postgresql+psycopg2://postgres:root@localhost:5432/common_admin"

# Create engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
