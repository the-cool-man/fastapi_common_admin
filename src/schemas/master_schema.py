from pydantic import BaseModel, field_validator
from fastapi import UploadFile
from ..utils import MultiFormatRequest
from typing import Optional
import os


MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}


class BannerSchema(BaseModel, MultiFormatRequest):
    id: Optional[int] = None
    status: str
    button_text: str
    link: str
    banner_title: str
    banner: UploadFile

    @field_validator("banner")
    def validate_images(cls, file: UploadFile):
        if not file:
            return file

        filename = file.filename.lower()
        ext = os.path.splitext(filename)[1]
        if ext not in ALLOWED_EXTENSIONS:
            raise ValueError(
                "banner must be .jpg, .jpeg, or .png files")

        file.file.seek(0, 2)
        size = file.file.tell()
        file.file.seek(0)
        if size > MAX_FILE_SIZE:
            raise ValueError("banner file size must be 5MB or less")
        return file

    @field_validator("link")
    def social_link_validate(cls, v):
        if not v.startswith(("http://", "https://")):
            raise ValueError("link must be valid URL")
        return v

    @field_validator("status")
    def status_validation(cls, v):
        if v not in ["A", "I"]:
            raise ValueError("Status Must Be A or I")
        return v


class CategorySchema(BaseModel, MultiFormatRequest):
    id: Optional[int] = None
    status: str
    category_name: str
    seo_title: str
    seo_keyword: str
    category_icon: UploadFile
    display_home_page: str
    seo_description: str

    @field_validator("category_icon")
    def validate_images(cls, file: UploadFile):
        if not file:
            return file

        filename = file.filename.lower()
        ext = os.path.splitext(filename)[1]
        if ext not in ALLOWED_EXTENSIONS:
            raise ValueError(
                "category_icon must be .jpg, .jpeg, or .png files")

        file.file.seek(0, 2)
        size = file.file.tell()
        file.file.seek(0)
        if size > MAX_FILE_SIZE:
            raise ValueError("category_icon file size must be 5MB or less")
        return file

    @field_validator("status")
    def status_validation(cls, v):
        if v not in ["A", "I"]:
            raise ValueError("Status Must Be A or I")
        return v

    @field_validator("display_home_page")
    def status_validation(cls, v):
        if v not in ["Y", "N"]:
            raise ValueError("display_home_page Must Be Y or N")
        return v


class CurrencySchema(BaseModel, MultiFormatRequest):
    id: Optional[int] = None
    status: str
    currency_name: str
    currency_code: str
    symbol: str

    @field_validator("status")
    def status_validation(cls, v):
        if v not in ["A", "I"]:
            raise ValueError("Status Must Be A or I")
        return v


class GstPercentageSchema(BaseModel, MultiFormatRequest):
    id: Optional[int] = None
    status: str
    gst_percentage: str

    @field_validator("status")
    def status_validation(cls, v):
        if v not in ["A", "I"]:
            raise ValueError("Status Must Be A or I")
        return v


class CountrySchema(BaseModel, MultiFormatRequest):
    id: Optional[int] = None
    status: str
    country_name: str
    country_code: str
    flag: Optional[str] = None

    @field_validator("status")
    def status_validation(cls, v):
        if v not in ["A", "I"]:
            raise ValueError("Status Must Be A or I")
        return v


class StateSchema(BaseModel, MultiFormatRequest):
    id: Optional[int] = None
    status: str
    country_id: str
    state_name: str

    @field_validator("status")
    def status_validation(cls, v):
        if v not in ["A", "I"]:
            raise ValueError("Status Must Be A or I")
        return v


class CitySchema(BaseModel, MultiFormatRequest):
    id: Optional[int] = None
    status: str
    city_name: str
    country_id: str
    state_id: str

    @field_validator("status")
    def status_validation(cls, v):
        if v not in ["A", "I"]:
            raise ValueError("Status Must Be A or I")
        return v
