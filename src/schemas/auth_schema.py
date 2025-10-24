
from pydantic import BaseModel, field_validator, ValidationError, model_validator
from fastapi import Form
from ..utils import MultiFormatRequest


class LoginSchema(BaseModel, MultiFormatRequest):
    email: str
    password: str

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


class ChangePassword(BaseModel, MultiFormatRequest):

    id: int
    password: str
    new_password: str
    confirm_password: str

    @model_validator(mode="after")
    def validate_fields(self):
        for field_name in ["password", "new_password", "confirm_password"]:
            value = getattr(self, field_name)
            if not (6 <= len(value) <= 8):
                
                raise ValueError(
                    f"{field_name} must be 6 to 8 characters long.")
        return self
