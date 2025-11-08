from sqlalchemy.sql import func
from ..db_connection import Base
from datetime import datetime, date
import enum
from src.utils.request_parser import BaseDic
from sqlalchemy import (
    Column, Integer, BigInteger, String, Enum, DateTime,
    TIMESTAMP, ForeignKey, Date, Text
)


class StatusEnum(str, enum.Enum):
    INACTIVE = "I"
    ACTIVE = "A"


class EmailTemplateModel(Base, BaseDic):

    __tablename__ = "email_templates"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    status = Column(
        Enum(StatusEnum, values_callable=lambda enum_cls: [
             e.value for e in enum_cls]),
        nullable=True,
        default=StatusEnum.INACTIVE
    )
    template_name = Column(String(200))
    email_subject = Column(String(255))
    email_content = Column(Text)
    deleted_at = Column(TIMESTAMP(timezone=True))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())


class SMSTemplateModel(Base, BaseDic):

    __tablename__ = "sms_templates"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    status = Column(
        Enum(StatusEnum, values_callable=lambda enum_cls: [
             e.value for e in enum_cls]),
        nullable=True,
        default=StatusEnum.INACTIVE
    )
    template_name = Column(String(200))
    sms_content = Column(Text)
    deleted_at = Column(TIMESTAMP(timezone=True))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())
