from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum,
    TIMESTAMP
)
from datetime import datetime, date
from decimal import Decimal

from ..db_connection import Base
import enum


class StatusEnum(str, enum.Enum):
    A = "A"
    I = "I"


class YesNoEnum(str, enum.Enum):
    Y = "Y"
    N = "N"


class AdminRole(Base):
    __tablename__ = "admin_role"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Enum(StatusEnum), nullable=False, default=StatusEnum.A)
    role_name = Column(String(255))
    site_setting = Column(Enum(YesNoEnum), nullable=False, default=YesNoEnum.N)
    banner = Column(Enum(YesNoEnum), nullable=False, default=YesNoEnum.N)
    category = Column(Enum(YesNoEnum), nullable=False, default=YesNoEnum.N)
    currency = Column(Enum(YesNoEnum), nullable=False, default=YesNoEnum.N)
    tax_data = Column(Enum(YesNoEnum), nullable=False, default=YesNoEnum.N)
    country = Column(Enum(YesNoEnum), nullable=False, default=YesNoEnum.N)
    state = Column(Enum(YesNoEnum), nullable=False, default=YesNoEnum.N)
    city = Column(Enum(YesNoEnum), nullable=False, default=YesNoEnum.N)
    media_gallery = Column(
        Enum(YesNoEnum), nullable=False, default=YesNoEnum.N)
    all_user = Column(Enum(YesNoEnum), nullable=False, default=YesNoEnum.N)
    chat = Column(Enum(YesNoEnum), nullable=False, default=YesNoEnum.N)
    rating = Column(Enum(YesNoEnum), nullable=False, default=YesNoEnum.N)
    site_content = Column(Enum(YesNoEnum), nullable=False, default=YesNoEnum.N)
    email_template = Column(
        Enum(YesNoEnum), nullable=False, default=YesNoEnum.N)
    sms_template = Column(Enum(YesNoEnum), nullable=False, default=YesNoEnum.N)
    rest_api = Column(Enum(YesNoEnum), nullable=False, default=YesNoEnum.N)
    payment_plan = Column(Enum(YesNoEnum), nullable=False, default=YesNoEnum.N)
    created_at = Column(TIMESTAMP(timezone=True))
    updated_at = Column(TIMESTAMP(timezone=True))
    deleted_at = Column(TIMESTAMP(timezone=True))

    def as_dict(self, base_url=None):

        result = {}
        for c in self.__table__.columns:
            value = getattr(self, c.name)
            if isinstance(value, (datetime, date)):
                result[c.name] = value.isoformat()
            elif isinstance(value, Decimal):
                result[c.name] = float(value)
            else:
                result[c.name] = value
        return result
