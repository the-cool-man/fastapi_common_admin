from .session import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends
from sqlalchemy.orm import declarative_base


def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



DBSession = Annotated[Session, Depends(db_session)]
Base = declarative_base()
