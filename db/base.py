# app/db/base.py
from sqlalchemy.orm import declarative_base


# This Base will be imported by models and Alembic
Base = declarative_base()
