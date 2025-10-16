
from pydantic import BaseModel, field_validator, ValidationError
from fastapi import Form
from utils import MultiFormatRequest


class LoginSchema(BaseModel, MultiFormatRequest):
    email: str
    password: str

    # @classmethod
    # def as_form(
    #     cls,
    #     email: str = Form(...),
    #     password: str = Form(...)
    # ):
    #     return cls(email=email, password=password)

    @field_validator("email")
    def email_must_have_at(cls, v):
        if "@" not in v:
            raise ValueError("Invalid email format")
        return v

    @field_validator("password")
    def password_min_length(cls, v):
        if len(v) < 6 or len(v) > 8:
            raise ValueError("Password must be between 6 and 8 characters")
        return v

