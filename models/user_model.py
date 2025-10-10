from sqlalchemy import Column, Integer, BigInteger, String, Enum, DateTime, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from db_connection.base import Base
import enum
from datetime import datetime, date
from decimal import Decimal


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
    status = Column(
        Enum(UserStatusEnum, values_callable=lambda enum_cls: [
            e.value for e in enum_cls]),
        nullable=False,
        default=UserStatusEnum.INACTIVE
    )
    username = Column(String(100))
    password = Column(String(100))
    c_password = Column(String(100))
    email = Column(String(50))
    phone = Column(String(25))
    ip_address = Column(String(50))
    last_login = Column(DateTime)
    register_ip = Column(String(50))
    register_ip_detail = Column(String(1000))
    user_type = Column(
        Enum(UserTypeEnum, values_callable=lambda enum_cls: [
            e.value for e in enum_cls]),
        nullable=False,
        default=UserTypeEnum.ADMIN
    )
    role = Column(Integer, ForeignKey("admin_role.id",
                                      ondelete="SET NULL"))  # FK to admin_role
    deleted_at = Column(TIMESTAMP(timezone=True))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())

    def as_dict(self, exclude_fields=None):
        if exclude_fields is None:
            exclude_fields = ['password', 'c_password']

        result = {}
        for c in self.__table__.columns:
            if c.name in exclude_fields:
                continue

            value = getattr(self, c.name)
            if isinstance(value, (datetime, date)):
                result[c.name] = value.isoformat()
            elif isinstance(value, Decimal):
                result[c.name] = float(value)
            else:
                result[c.name] = value
        return result
