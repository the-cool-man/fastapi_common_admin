# app/db/session.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
load_dotenv()

# Replace with your actual Postgres credentials
# DATABASE_URL = "postgresql+psycopg2://postgres:root@localhost:5432/common_admin"
# DATABASE_URL = "postgresql://postgres:root@localhost:5432/common_admin"

DATABASE_URL = os.getenv("DB_CONNECTION_URL")

# Create engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
