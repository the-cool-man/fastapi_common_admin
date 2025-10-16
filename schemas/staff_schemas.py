from pydantic import BaseModel, field_validator, ValidationError
from typing import Optional
from utils import MultiFormatRequest


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
    def status_validation(cls, v):
        if v not in ["A", "S", "P"]:
            raise ValueError("Status Must Be A or S or P")
        return v


class StaffListSchema(BaseModel, MultiFormatRequest):
    sort_order: Optional[str] = "DESC"
    sort_column: Optional[str] = "id"
    search_field: Optional[str] = None
    limit_per_page: Optional[int] = 10
    page: Optional[int] = 1
    status_update: Optional[str] = "A"
    checkbox_val: Optional[list] = []
