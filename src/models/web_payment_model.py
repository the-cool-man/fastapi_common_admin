from sqlalchemy import (
    Column, Integer, BigInteger, String, Enum, DateTime,
    TIMESTAMP, ForeignKey, Date, Text
)
from sqlalchemy.sql import func
from ..db_connection import Base
from datetime import datetime, date
import enum
from src.utils.request_parser import BaseDic


class StatusEnum(str, enum.Enum):
    INACTIVE = "I"
    ACTIVE = "A"

class MessageCurrentEnum(str, enum.Enum):
    YES = "Y"
    NO = "N"


class WebServiceModel(Base, BaseDic):
    __tablename__ = "web_service"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    service_name = Column(String(100))
    service_url = Column(String(100))
    method = Column(String(100))
    description = Column(Text)
    parameter = Column(Text)
    success_response = Column(Text)
    error_response = Column(Text)
    status = Column(
        Enum(StatusEnum, values_callable=lambda enum_cls: [
             e.value for e in enum_cls]),
        nullable=True,
        default=StatusEnum.INACTIVE
    )

    deleted_at = Column(TIMESTAMP(timezone=True))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())


class UserPaymentModel(Base, BaseDic):
    __tablename__ = "user_payment"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    name = Column(String(100))
    email = Column(String(100))
    mobile = Column(String(15))
    plan_name = Column(String(50))
    contact_limit = Column(Text)
    parameter = Column(Text)
    success_response = Column(Integer)
    used_contact_limit = Column(Integer)
    plan_duration = Column(Integer)
    plan_offers = Column(Text)
    payment_mode = Column(Integer)
    payment_note = Column(Text)
    transaction_id = Column(String(100))
    coupon_code = Column(String(50))
    discount_percentage = Column(String(50))
    currency = Column(String(50))
    plan_amount = Column(String(50))
    plan_type = Column(String(50))
    discount_amount = Column(String(50))
    total_amount = Column(String(50))
    status = Column(
        Enum(StatusEnum, values_callable=lambda enum_cls: [
             e.value for e in enum_cls]),
        nullable=True,
        default=StatusEnum.INACTIVE
    )
    message_allow = Column(
        Enum(MessageCurrentEnum, values_callable=lambda enum_cls: [
             e.value for e in enum_cls]),
        nullable=True,
        default=MessageCurrentEnum.NO
    )
    current_plan = Column(
        Enum(MessageCurrentEnum, values_callable=lambda enum_cls: [
             e.value for e in enum_cls]),
        nullable=True,
        default=MessageCurrentEnum.NO
    )

    active_date = Column(TIMESTAMP(timezone=True))
    expiry_date = Column(TIMESTAMP(timezone=True))
    deleted_at = Column(TIMESTAMP(timezone=True))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())
