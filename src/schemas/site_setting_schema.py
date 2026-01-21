from fastapi import UploadFile
from pydantic import BaseModel, field_validator, model_validator, ValidationError, model_validator
from ..utils import MultiFormatRequest
from typing import Optional, Union
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
            if not values.logo and not values.favicon:
                raise ValueError(
                    "logo or favicon are required")
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


class EmailUpdate(BaseModel, MultiFormatRequest):
    id: Optional[Union[int, str]] = None
    flag: Optional[str] = None
    contact_email: Optional[str] = None
    from_email: Optional[str] = None


class SocialMediaSchema(BaseModel, MultiFormatRequest):
    id: Optional[int] = None
    social_name: str
    social_link: str
    social_logo: UploadFile
    status: str

    @field_validator("social_link")
    def social_link_validate(cls, v):
        if not v.startswith(("http://", "https://")):
            raise ValueError("social_link must be valid URL")
        return v

    @field_validator("social_logo")
    def validate_images(cls, file: UploadFile):
        if not file:
            return file

        filename = file.filename.lower()
        ext = os.path.splitext(filename)[1]
        if ext not in ALLOWED_EXTENSIONS:
            raise ValueError(
                "social_logo must be .jpg, .jpeg, or .png files")

        file.file.seek(0, 2)
        size = file.file.tell()
        file.file.seek(0)
        if size > MAX_FILE_SIZE:
            raise ValueError("social_logo file size must be 5MB or less")
        return file

    @field_validator("status")
    def status_validation(cls, v):
        if v not in ["A", "I"]:
            raise ValueError("Status Must Be A or I")
        return v


class StaffAddSchema(BaseModel, MultiFormatRequest):

    id: Optional[int] = None
    username: str
    email: str
    password: str
    user_type: str
    role: str
    status: str

    @field_validator("email")
    def email_validation(cls, v):
        if "@" not in v:
            raise ValueError("Invalid email format")
        return v

    @field_validator("password")
    def password_validation(cls, v):
        if len(v) < 6 or len(v) > 8:
            raise ValueError("Password must be between 6 and 8 characters")
        return v

    @field_validator("status")
    def status_validation(cls, v):
        if v not in ["A", "I"]:
            raise ValueError("Status Must Be A or I")
        return v

    @field_validator("user_type")
    def user_type_validation(cls, v):
        if v not in ["A", "S", "P"]:
            raise ValueError("Status Must Be A or S or P")
        return v


class StaffRoleSchema(BaseModel, MultiFormatRequest):

    id: Optional[int] = None
    status: str
    role_name: str
    site_setting: str
    banner: str
    category: str
    currency: str
    tax_data: str
    country: str
    state: str
    city: str
    media_gallery: str
    all_user: str
    chat: str
    rating: str
    site_content: str
    email_template: str
    sms_template: str
    rest_api: str
    payment_plan: str

    @field_validator("status")
    def status_validation(cls, v):
        if v not in ["A", "I"]:
            raise ValueError("Status Must Be A or I")
        return v

    @model_validator(mode='after')
    def check_value_type(self):
        required_key = [
            "site_setting",
            "banner",
            "category",
            "currency",
            "tax_data",
            "country",
            "state",
            "city",
            "media_gallery",
            "all_user",
            "chat",
            "rating",
            "site_content",
            "email_template",
            "sms_template",
            "rest_api",
            "payment_plan"
        ]

        status_missing = [field for field in required_key if getattr(
            self, field) is None]

        if status_missing:
            raise ValueError(
                f"The following fields are must be Y or N: {', '.join(status_missing)}"
            )
        return self


class PublicPageSEOSchema(BaseModel, MultiFormatRequest):
    id: Optional[int] = None
    page_name: str
    meta_title: str
    meta_description: str
    meta_image: UploadFile
    status: str

    @field_validator("meta_image")
    def validate_images(cls, file: UploadFile):
        if not file:
            return file

        filename = file.filename.lower()
        ext = os.path.splitext(filename)[1]
        if ext not in ALLOWED_EXTENSIONS:
            raise ValueError(
                "meta_image must be .jpg, .jpeg, or .png files")

        file.file.seek(0, 2)
        size = file.file.tell()
        file.file.seek(0)
        if size > MAX_FILE_SIZE:
            raise ValueError("meta_image file size must be 5MB or less")
        return file

    @field_validator("status")
    def status_validation(cls, v):
        if v not in ["A", "I"]:
            raise ValueError("Status Must Be A or I")
        return v
