
from ..utils import bcrypt_context
from ..models import EmailTemplateModel as EmailTemplate
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
import os
import time
import uuid
from pathlib import Path
from datetime import datetime


async def handleEmailTemplate(request_data, db):

    try:
        if request_data.id is None:
            is_name_exist = db.query(EmailTemplate).filter(
                EmailTemplate.template_name == request_data.template_name
            ).first()
            if is_name_exist:
                return JSONResponse(
                    content={"status": "error",
                             "message": "template_name has already been taken."},
                    status_code=200
                )
            model_data = EmailTemplate()
            message = "inserted"
        else:
            model_data = db.query(EmailTemplate).filter(
                EmailTemplate.id == request_data.id
            ).first()

            if not model_data:
                return JSONResponse(
                    content={"status": "error",
                             "message": "Record not found!"},
                    status_code=200
                )
            if db.query(EmailTemplate).filter(
                EmailTemplate.template_name == request_data.template_name, EmailTemplate.id != request_data.id
            ).first():
                return JSONResponse(
                    content={"status": "error",
                             "message": "template_name has already been taken."},
                    status_code=200
                )

            message = "updated"

        model_data.template_name = request_data.template_name
        model_data.email_subject = request_data.email_subject
        model_data.email_content = request_data.email_content
        model_data.status = request_data.status

        db.add(model_data)
        db.commit()
        db.refresh(model_data)

        return JSONResponse(
            content={
                "status": "success",
                "message": f"Email Template {message} successfully",
            },
            status_code=200
        )

    except Exception as err:
        db.rollback()
        return JSONResponse(
            content={"status": "error", "message": str(err)},
            status_code=200
        )

