from pydantic import BaseModel, field_validator
from fastapi import UploadFile
from typing import Optional
from ..utils import MultiFormatRequest
import os


class WebServiceSchema(BaseModel, MultiFormatRequest):

    id: Optional[int] = None
    status: str
    service_name: str
    service_url: str
    success_response: str
    error_response: str
    description: str
    method: str
    parameter: str

    @field_validator("status")
    def status_validation(cls, v):
        if v not in ["A", "I"]:
            raise ValueError("Status Must Be A or I")
        return v

    @field_validator("service_url")
    def social_link_validate(cls, v):
        if not v.startswith(("http://", "https://")):
            raise ValueError("service_url must be valid URL")
        return v

class MembershipPlanSchema(BaseModel, MultiFormatRequest):

    id: Optional[int] = None
    status: str
    plan_name: str
    plan_offers: str
    plan_duration: str
    plan_amount: str
    message_allow: str
    currency: str
    contact_limit: str
    plan_type: str

    @field_validator("status")
    def status_validation(cls, v):
        if v not in ["A", "I"]:
            raise ValueError("Status Must Be A or I")
        return v


class CouponSchema(BaseModel, MultiFormatRequest):

    id: Optional[int] = None
    status: str
    coupon_code: str
    discount_percentage: str
    expiry_date: str
    max_discount_amount: str
    max_per_user_limit: str
    total_user_limit: str

    @field_validator("status")
    def status_validation(cls, v):
        if v not in ["A", "I"]:
            raise ValueError("Status Must Be A or I")
        return v


