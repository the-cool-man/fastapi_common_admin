from db_connection.session import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends


def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DBSession = Annotated[Session, Depends(db_session)]
