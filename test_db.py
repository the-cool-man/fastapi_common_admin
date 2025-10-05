# app/test_db.py
from db.session import SessionLocal
from models.admin_role import AdminRole

db = SessionLocal()
roles = db.query(AdminRole).all()
print(roles)
