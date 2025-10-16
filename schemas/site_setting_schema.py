from fastapi import UploadFile
from pydantic import BaseModel, field_validator, model_validator, ValidationError
from utils import MultiFormatRequest
from typing import Optional
from fastapi import UploadFile, Form
import os


MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}


class LogoFavSchema(BaseModel, MultiFormatRequest):
    id: Optional[int] = None
    favicon: Optional[UploadFile] = None
    logo: Optional[UploadFile] = None
    flag: Optional[str] = None

    @field_validator("logo", "favicon")
    def validate_images(cls, file: UploadFile):
        if not file:
            return file

        filename = file.filename.lower()
        ext = os.path.splitext(filename)[1]
        if ext not in ALLOWED_EXTENSIONS:
            raise ValueError(
                "logo or favicon must be .jpg, .jpeg, or .png files")

        file.file.seek(0, 2)
        size = file.file.tell()
        file.file.seek(0)
        if size > MAX_FILE_SIZE:
            raise ValueError("logo or favicon file size must be 5MB or less")
        return file

    @model_validator(mode="after")
    def check_required_files(cls, values):
        if values.flag == "logo_fav":
            if not values.logo or not values.favicon:
                raise ValueError(
                    "logo and favicon are required")
        return values


class CommonSetting(BaseModel, MultiFormatRequest):
    id: Optional[str] = None
    flag: Optional[str] = None
    contact_no: Optional[str] = None
    google_analytics_code: Optional[str] = None
    footer_text: Optional[str] = None
    about_footer: Optional[str] = None
    full_address: Optional[str] = None
    web_name: Optional[str] = None
    web_frienly_name: Optional[str] = None
    website_title: Optional[str] = None
    website_description: Optional[str] = None
    website_keywords: Optional[str] = None
    map_address: Optional[str] = None
    timezone: Optional[str] = None

    @model_validator(mode="after")
    def check_required_for_basic_setting(self):
        if self.flag == "basic_setting":
            required_fields = [
                "contact_no", "footer_text", "about_footer", "full_address",
                "web_name", "web_frienly_name", "website_title",
                "website_description", "website_keywords", "map_address", "timezone"
            ]
            missing = [field for field in required_fields if getattr(
                self, field) is None]
            if missing:
                raise ValueError(
                    f"The following fields are required': {', '.join(missing)}"
                )
        return self


class SiteConfigSchema(BaseModel, MultiFormatRequest):
    id: Optional[int] = None
    status: str = "A"
    web_name: Optional[str] = None
    web_frienly_name: Optional[str] = None
    contact_no: Optional[str] = None
    website_title: Optional[str] = None
    website_description: Optional[str] = None
    website_keywords: Optional[str] = None
    google_analytics_code: Optional[str] = None
    footer_text: Optional[str] = None
    about_footer: Optional[str] = None
    from_email: Optional[str] = None
    contact_email: Optional[str] = None
    full_address: Optional[str] = None
    map_address: Optional[str] = None
    sms_api: Optional[str] = None
    sms_api_status: Optional[str] = None
    android_app_link: Optional[str] = None
    ios_app_link: Optional[str] = None
    current_date_crone: Optional[str] = None
    timezone: Optional[str] = None
    smtp_host: Optional[str] = None
    smtp_port: Optional[str] = None
    smtp_user: Optional[str] = None
    smtp_pass: Optional[str] = None

    @field_validator("status")
    def status_validation(cls, v):
        if v not in ["A", "I"]:
            raise ValueError("Status must be A or I")
        return v
