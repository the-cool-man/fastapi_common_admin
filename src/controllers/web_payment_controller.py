from ..utils import bcrypt_context
from ..models import WebServiceModel as WebService, UserPaymentModel as UserPayment
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
import os
import time
import uuid
from pathlib import Path
from datetime import datetime


def parse_expiryDate(date_str: str):
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    raise ValueError("Invalid date format. Use YYYY-MM-DD or DD/MM/YYYY.")


async def handleWebServiceSave(request_data, db):
    try:
        if request_data.id is None:
            if db.query(WebService).filter(WebService.service_name == request_data.service_name).first():
                return JSONResponse(
                    content={"status": "error",
                             "message": "service_name has already been taken"},
                    status_code=200
                )
            model_data = WebService()
            message = "Inserted"

        else:
            model_data = db.query(WebService).filter(
                WebService.id == request_data.id).first()
            if not model_data:
                return JSONResponse(
                    content={"status": "error",
                             "message": "Record Not Found For Update"},
                    status_code=200
                )

            if (
                model_data.service_name != request_data.service_name
                and db.query(WebService).filter(WebService.service_name == request_data.service_name).first()
            ):
                return JSONResponse(
                    content={"status": "error",
                             "message": "service_name has already been taken"},
                    status_code=200
                )
            message = "Updated"

        model_data.status = request_data.status
        model_data.service_name = request_data.service_name
        model_data.service_url = request_data.service_url
        model_data.success_response = request_data.success_response
        model_data.error_response = request_data.error_response
        model_data.description = request_data.description
        model_data.method = request_data.method
        model_data.parameter = request_data.parameter

        db.add(model_data)
        db.commit()

        return JSONResponse(
            content={"status": "success",
                     "message": f"Web Service {message} successfully"},
            status_code=200
        )

    except Exception as err:
        db.rollback()
        return JSONResponse(
            content={"status": "error", "message": f"ad{str(err)}"},
            status_code=200
        )


async def handleMembershipPlanSave(request_data, db):
    try:
        if request_data.id is None:
            if db.query(UserPayment).filter(UserPayment.plan_name == request_data.plan_name).first():
                return JSONResponse(
                    content={"status": "error",
                             "message": "plan_name has already been taken"},
                    status_code=200
                )
            model_data = UserPayment()
            message = "Inserted"

        else:
            model_data = db.query(UserPayment).filter(
                UserPayment.id == request_data.id).first()
            if not model_data:
                return JSONResponse(
                    content={"status": "error",
                             "message": "Record Not Found For Update"},
                    status_code=200
                )

            if (
                model_data.plan_name != request_data.plan_name
                and db.query(UserPayment).filter(UserPayment.plan_name == request_data.plan_name).first()
            ):
                return JSONResponse(
                    content={"status": "error",
                             "message": "plan_name has already been taken"},
                    status_code=200
                )
            message = "Updated"

        model_data.status = request_data.status
        model_data.discount_percentage = request_data.discount_percentage
        model_data.plan_offers = request_data.plan_offers
        model_data.plan_duration = request_data.plan_duration
        model_data.plan_amount = request_data.plan_amount
        model_data.message_allow = request_data.message_allow
        model_data.currency = request_data.currency
        model_data.contact_limit = request_data.contact_limit
        model_data.plan_type = request_data.plan_type

        db.add(model_data)
        db.commit()

        return JSONResponse(
            content={"status": "success",
                     "message": f"Membership Plan {message} successfully"},
            status_code=200
        )

    except Exception as err:
        db.rollback()
        return JSONResponse(
            content={"status": "error", "message": f"ad{str(err)}"},
            status_code=200
        )


async def handleCouponSave(request_data, db):
    try:
        if request_data.id is None:
            if db.query(UserPayment).filter(UserPayment.coupon_code == request_data.coupon_code).first():
                return JSONResponse(
                    content={"status": "error",
                             "message": "coupon_code has already been taken"},
                    status_code=200
                )
            model_data = UserPayment()
            message = "Inserted"

        else:
            model_data = db.query(UserPayment).filter(
                UserPayment.id == request_data.id).first()
            if not model_data:
                return JSONResponse(
                    content={"status": "error",
                             "message": "Record Not Found For Update"},
                    status_code=200
                )

            if (
                model_data.coupon_code != request_data.coupon_code
                and db.query(UserPayment).filter(UserPayment.coupon_code == request_data.coupon_code).first()
            ):
                return JSONResponse(
                    content={"status": "error",
                             "message": "coupon_code has already been taken"},
                    status_code=200
                )
            message = "Updated"

        model_data.status = request_data.status
        model_data.coupon_code = request_data.coupon_code
        model_data.expiry_date = parse_expiryDate(request_data.expiry_date)
        model_data.discount_amount = request_data.max_discount_amount
        model_data.contact_limit = request_data.max_per_user_limit
        model_data.used_contact_limit = request_data.total_user_limit
        model_data.discount_percentage = request_data.discount_percentage

        db.add(model_data)
        db.commit()

        return JSONResponse(
            content={"status": "success",
                     "message": f"Coupon {message} successfully"},
            status_code=200
        )

    except Exception as err:
        db.rollback()
        return JSONResponse(
            content={"status": "error", "message": f"ad{str(err)}"},
            status_code=200
        )
