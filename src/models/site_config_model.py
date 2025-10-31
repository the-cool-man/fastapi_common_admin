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


class SiteConfig(Base):
    __tablename__ = "site_config"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    status = Column(
        Enum(StatusEnum, values_callable=lambda enum_cls: [
             e.value for e in enum_cls]),
        nullable=False,
        default=StatusEnum.INACTIVE
    )

    web_name = Column(String(200))
    web_frienly_name = Column(String(100))
    logo = Column(String(100))
    favicon = Column(String(100))
    contact_no = Column(String(50))
    website_title = Column(String(100))
    website_description = Column(String(500))
    website_keywords = Column(String(500))
    google_analytics_code = Column(String(500))
    footer_text = Column(String(500))
    about_footer = Column(String(500))
    from_email = Column(String(50))
    contact_email = Column(String(50))
    full_address = Column(String(500))
    map_address = Column(Text)
    sms_api = Column(String(500))
    sms_api_status = Column(
        Enum(StatusEnum, values_callable=lambda enum_cls: [
             e.value for e in enum_cls]),
        nullable=False,
        default=StatusEnum.INACTIVE
    )
    android_app_link = Column(String(100))
    ios_app_link = Column(String(100))
    current_date_crone = Column(DateTime)
    timezone = Column(String(100))
    smtp_host = Column(Text)
    smtp_port = Column(String(50))
    smtp_user = Column(Text)
    smtp_pass = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())
    deleted_at = Column(TIMESTAMP(timezone=True))

    def as_dict(self, exclude_fields=None, base_url=None):
        if exclude_fields is None:
            exclude_fields = []

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

    # Add full URLs if base_url is provided
        if base_url:
            result["logo_full_url"] = f"{base_url}/logos/{self.logo}" if self.logo else None
            result["favicon_full_url"] = f"{base_url}/favicons/{self.favicon}" if self.favicon else None

        return result


class SocialMedia(Base, BaseDic):
    __tablename__ = "social_networking_links"
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    status = Column(
        Enum(StatusEnum, values_callable=lambda enum_cls: [
             e.value for e in enum_cls]),
        nullable=False,
        default=StatusEnum.INACTIVE
    )
    social_name = Column(String(50))
    social_link = Column(String(200))
    social_logo = Column(String(100))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())
    deleted_at = Column(TIMESTAMP(timezone=True))
    


class PublicPageSEO(Base, BaseDic):
    __tablename__ = "public_pages_seo"
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    status = Column(
        Enum(StatusEnum, values_callable=lambda enum_cls: [
             e.value for e in enum_cls]),
        nullable=False,
        default=StatusEnum.INACTIVE
    )
    page_name = Column(String(50))
    meta_title = Column(String(200))
    meta_description = Column(String(300))
    meta_image = Column(String(100))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())
    deleted_at = Column(TIMESTAMP(timezone=True))
