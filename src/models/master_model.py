from datetime import datetime, date
from decimal import Decimal
from ..db_connection import Base
from sqlalchemy import Column, Integer, BigInteger, String, Enum, DateTime, TIMESTAMP, ForeignKey, Text
from sqlalchemy.sql import func
import enum
from src.utils.request_parser import BaseDic


class StatusEnum(str, enum.Enum):
    INACTIVE = "I"
    ACTIVE = "A"


class DisplayHomePageEnum(str, enum.Enum):
    YES = "Y"
    NO = "N"


class BannerModel(Base, BaseDic):
    __tablename__ = "banner_master"
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    status = Column(
        Enum(StatusEnum, values_callable=lambda enum_cls: [
             e.value for e in enum_cls]),
        nullable=False,
        default=StatusEnum.INACTIVE
    )
    banner_title = Column(String(50))
    link = Column(String(200))
    button_text = Column(String(200))
    banner = Column(String(100))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())
    deleted_at = Column(TIMESTAMP(timezone=True))


class CategoryModel(Base, BaseDic):
    __tablename__ = "category"
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    status = Column(
        Enum(StatusEnum, values_callable=lambda enum_cls: [
             e.value for e in enum_cls]),
        nullable=False,
        default=StatusEnum.INACTIVE
    )
    category_name = Column(String(50))
    seo_title = Column(String(50))
    seo_keyword = Column(String(50))
    display_home_page = Column(
        Enum(DisplayHomePageEnum, values_callable=lambda enum_cls: [
             e.value for e in enum_cls]),
        nullable=False,
        default=DisplayHomePageEnum.NO
    )
    seo_description = Column(String(200))
    category_icon = Column(String(100))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())
    deleted_at = Column(TIMESTAMP(timezone=True))


class CurrencyModel(Base, BaseDic):
    __tablename__ = "currency_master"
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    status = Column(
        Enum(StatusEnum, values_callable=lambda enum_cls: [
             e.value for e in enum_cls]),
        nullable=False,
        default=StatusEnum.INACTIVE
    )
    currency_name = Column(String(100))
    currency_code = Column(String(100))
    symbol = Column(String(10))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())
    deleted_at = Column(TIMESTAMP(timezone=True))


class GstPercentageModel(Base, BaseDic):
    __tablename__ = "gst_percentage"
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    status = Column(
        Enum(StatusEnum, values_callable=lambda enum_cls: [
             e.value for e in enum_cls]),
        nullable=False,
        default=StatusEnum.INACTIVE
    )
    gst_percentage = Column(String(10))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())
    deleted_at = Column(TIMESTAMP(timezone=True))
