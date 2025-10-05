from sqlalchemy import Column, Integer, BigInteger, String, Enum, DateTime, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from db.base import Base
import enum


class UserStatusEnum(str, enum.Enum):
    INACTIVE = "I"
    ACTIVE = "A"


class UserTypeEnum(str, enum.Enum):
    SUPERADMIN = "S"
    ADMIN = "A"
    PARTNER = "P"


class AdminUser(Base):
    __tablename__ = "admin_users"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    status = Column(Enum(UserStatusEnum), nullable=False, default=UserStatusEnum.INACTIVE)
    username = Column(String(100))
    password = Column(String(100))
    c_password = Column(String(100))
    email = Column(String(50))
    phone = Column(String(25))
    ip_address = Column(String(50))
    last_login = Column(DateTime)
    register_ip = Column(String(50))
    register_ip_detail = Column(String(1000))
    user_type = Column(Enum(UserTypeEnum), nullable=False, default=UserTypeEnum.ADMIN)
    role = Column(Integer, ForeignKey("admin_role.id", ondelete="SET NULL"))  # FK to admin_role
    deleted_at = Column(TIMESTAMP(timezone=True))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())
