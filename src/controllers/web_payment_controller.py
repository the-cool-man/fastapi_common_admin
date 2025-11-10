from ..utils import bcrypt_context
from ..models import WebServiceModel as WebService
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
import os
import time
import uuid
from pathlib import Path
from datetime import datetime

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
