from pydantic import BaseModel, field_validator
from fastapi import UploadFile
from typing import Optional
from ..utils import MultiFormatRequest, BaseManualSchema
import os


MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}


class OrdinaryUserSchema(BaseManualSchema, MultiFormatRequest):
    id: Optional[int] = None
    name: str
    email: str
    password: str
    birthdate: str
    contact_number: int
    # remember_token: Optional[str]
    # email_verified_at: Optional[str]
    # user_id: str
    gender: str
    country_id: int
    state_id: int
    city_id: int
    photo: UploadFile
    photo_approve: str
    status: str

    @field_validator("gender")
    def status_validation(cls, v):
        if v not in ["Male", "Female"]:
            raise ValueError("gender Must Be Male or Female")
        return v

    @field_validator("photo_approve")
    def status_validation(cls, v):
        if v not in ["A", "I", "P"]:
            raise ValueError("Status Must Be A or I or P")
        return v

    @field_validator("photo")
    def validate_images(cls, file: UploadFile):
        if not file:
            return file

        filename = file.filename.lower()
        ext = os.path.splitext(filename)[1]
        if ext not in ALLOWED_EXTENSIONS:
            raise ValueError(
                "photo must be .jpg, .jpeg, or .png files")

        file.file.seek(0, 2)
        size = file.file.tell()
        file.file.seek(0)
        if size > MAX_FILE_SIZE:
            raise ValueError("photo file size must be 5MB or less")
        return file

    @field_validator("status")
    def status_validation(cls, v):
        if v not in ["A", "I"]:
            raise ValueError("Status Must Be A or I")
        return v

    @field_validator("password")
    def password_min_length(cls, v):
        if v is None:
            raise ValueError("Password is Required")

        if len(v) < 6 or len(v) > 8:
            raise ValueError("Password must be between 6 and 8 characters")
        return v


class MediaGallerySchema(BaseManualSchema, MultiFormatRequest):

    id: Optional[int] = None
    status: str
    media_name: UploadFile

    # @field_validator("id", mode="before")
    # def validate_id(cls, v):
    #     if v in ("", " ", None):
    #         return None
    #     try:
    #         return int(v)
    #     except:
    #         raise ValueError("id must be an integer or null")

    @field_validator("media_name")
    def validate_images(cls, file: UploadFile):
        if not file:
            return file

        filename = file.filename.lower()
        ext = os.path.splitext(filename)[1]
        if ext not in ALLOWED_EXTENSIONS:
            raise ValueError(
                "media_name must be .jpg, .jpeg, or .png files"
            )

        file.file.seek(0, 2)
        size = file.file.tell()
        file.file.seek(0)

        if size > MAX_FILE_SIZE:
            raise ValueError("media_name file size must be 5MB or less")
        return file

    @field_validator("status")
    def status_validation(cls, v):
        if v not in ["A", "I"]:
            raise ValueError("Status Must Be A or I")
        return v


class CmsPageSchema(BaseManualSchema, MultiFormatRequest):

    id: Optional[int] = None
    status: str
    meta_image: UploadFile
    page_title: str
    page_content: str
    meta_title: str
    meta_description: str
    display_footer: str

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

    @field_validator("display_footer")
    def status_validation(cls, v):
        if v not in ["Y", "N"]:
            raise ValueError("Status Must Be Y or N")
        return v
