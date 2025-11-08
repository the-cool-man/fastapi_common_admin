from sqlalchemy import (
    Column, Integer, BigInteger, String, Enum, DateTime,
    TIMESTAMP, ForeignKey, Date, Text
)
from sqlalchemy.sql import func
from ..db_connection import Base
from datetime import datetime, date
import enum
from src.utils.request_parser import BaseDic


# -------------------------
# ENUMS
# -------------------------
class StatusEnum(str, enum.Enum):
    INACTIVE = "I"
    ACTIVE = "A"


class GenderEnum(str, enum.Enum):
    MALE = "Male"
    FEMALE = "Female"


class PhotoApproveEnum(str, enum.Enum):
    INACTIVE = "I"
    ACTIVE = "A"
    PENDING = "P"


class DisplayFooterEnum(str, enum.Enum):
    YES = "Y"
    NO = "N"


class OrdinaryUserModel(Base, BaseDic):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    name = Column(String(100))
    email = Column(String(100))
    status = Column(
        Enum(StatusEnum, values_callable=lambda enum_cls: [
             e.value for e in enum_cls]),
        nullable=True,
        default=StatusEnum.INACTIVE
    )
    birthdate = Column(Date)
    email_verified_at = Column(TIMESTAMP)
    password = Column(String(100))
    remember_token = Column(String(100))
    contact_number = Column(String(200))
    contact_number_verified_at = Column(TIMESTAMP)
    device_token = Column(Text)
    deleted_at = Column(TIMESTAMP(timezone=True))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())


class OrdinaryUserDetailModel(Base, BaseDic):
    __tablename__ = "user_details"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    country_id = Column(Integer)
    state_id = Column(Integer)
    city_id = Column(Integer)
    address = Column(String(255))
    photo = Column(String(100))

    gender = Column(
        Enum(GenderEnum, values_callable=lambda enum_cls: [
             e.value for e in enum_cls]),
        nullable=True,
        default=GenderEnum.MALE
    )
    photo_approve = Column(
        Enum(PhotoApproveEnum, values_callable=lambda enum_cls: [
             e.value for e in enum_cls]),
        nullable=True,
        default=PhotoApproveEnum.PENDING
    )

    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="SET NULL"))

    deleted_at = Column(TIMESTAMP(timezone=True))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())


class OrdinaryUserRatingModel(Base, BaseDic):
    __tablename__ = "user_ratings"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    rating = Column(Integer)
    posted_id = Column(Integer)
    message = Column(Text)
    status = Column(
        Enum(StatusEnum, values_callable=lambda enum_cls: [
             e.value for e in enum_cls]),
        nullable=True,
        default=StatusEnum.INACTIVE
    )
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="SET NULL"))

    deleted_at = Column(TIMESTAMP(timezone=True))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())


class MediaGalleryModel(Base, BaseDic):
    __tablename__ = "photo_gallery"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="SET NULL"))
    status = Column(
        Enum(StatusEnum, values_callable=lambda enum_cls: [
             e.value for e in enum_cls]),
        nullable=True,
        default=StatusEnum.INACTIVE
    )
    media_name = Column(String(100))
    deleted_at = Column(TIMESTAMP(timezone=True))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())


class CmsPageModel(Base, BaseDic):
    __tablename__ = "cms_pages"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    status = Column(
        Enum(StatusEnum, values_callable=lambda enum_cls: [
             e.value for e in enum_cls]),
        nullable=True,
        default=StatusEnum.INACTIVE
    )
    display_footer = Column(
        Enum(DisplayFooterEnum, values_callable=lambda enum_cls: [
             e.value for e in enum_cls]),
        nullable=True,
        default=DisplayFooterEnum.NO
    )
    page_title = Column(String(200))
    alias = Column(String(200))
    page_content = Column(Text)
    meta_title = Column(String(200))
    meta_description = Column(String(200))
    meta_image = Column(String(100))
    deleted_at = Column(TIMESTAMP(timezone=True))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())
