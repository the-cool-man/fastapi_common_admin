
from pydantic import BaseModel, field_validator
from fastapi import UploadFile
from typing import Optional
from ..utils import MultiFormatRequest
import os


class EmailTemplateSchema(BaseModel, MultiFormatRequest):

    id: Optional[int] = None
    status: str
    template_name: str
    email_subject: str
    email_content: str

    @field_validator("status")
    def status_validation(cls, v):
        if v not in ["A", "I"]:
            raise ValueError("Status Must Be A or I")
        return v

class SMSTemplateSchema(BaseModel, MultiFormatRequest):

    id: Optional[int] = None
    status: str
    sms_content: str
    template_name: str

    @field_validator("status")
    def status_validation(cls, v):
        if v not in ["A", "I"]:
            raise ValueError("Status Must Be A or I")
        return v
