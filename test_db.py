# app/test_db.py
from db_connection.session import SessionLocal
from models.admin_role_model import AdminRole

db = SessionLocal()
roles = db.query(AdminRole).all()
print(roles)
