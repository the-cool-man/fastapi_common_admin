
from fastapi import APIRouter, Depends, Request, Query, Request
from fastapi.responses import JSONResponse
from typing import Annotated
from ..models import EmailTemplateModel as EmailTemplate, SMSTemplateModel as SmsTemplate
from ..schemas import ListDataSchema, EmailTemplateSchema, SMSTemplateSchema
from ..db_connection import DBSession
from ..utils import validate_token, status_update, check_token_response, sort_search_paginate_data, edit_data
from ..controllers import handleEmailTemplate, handleSMSTemplate
import os
from pathlib import Path
import json

router = APIRouter()


# EMAIL TEMPLATE ROUTE ----------------------------

@router.post("/email-template-list")
def get_email_template_data(request_data: Annotated[ListDataSchema, Depends(ListDataSchema.from_request)], db: DBSession, page: int = Query(1, g=1), valid_token=Depends(validate_token)):

    if (res := check_token_response(valid_token)):
        return res

    # STATUS UPDATE -------------------------

    if request_data.status_update in ["A", "I", "DELETE"] and len(request_data.checkbox_val) > 0:
        return status_update(request_data, db, EmailTemplate)

    # SORTING, SEARCHING AND PAGINATION -------------------------

    query = db.query(EmailTemplate)
    response_data = sort_search_paginate_data(
        request_data, db, EmailTemplate, query, page, search_column="template_name")

    return JSONResponse(content=response_data, status_code=200)


@router.post("/email-template-save")
async def add_email_template(
    request_data: Annotated[EmailTemplateSchema, Depends(EmailTemplateSchema.from_request)],
    db: DBSession,
    valid_token=Depends(validate_token)
):
    if (res := check_token_response(valid_token)):
        return res

    return await handleEmailTemplate(request_data, db)


@router.get("/email-template-list/edit/{edit_id}")
def email_template_edit_data(edit_id: int, db: DBSession, valid_token=Depends(validate_token)):

    if (res := check_token_response(valid_token)):
        return res

    return edit_data(db, EmailTemplate, edit_id)


# SMS TEMPLATE ROUTE ----------------------------


@router.post("/sms-template-list")
def get_sms_template_data(request_data: Annotated[ListDataSchema, Depends(ListDataSchema.from_request)], db: DBSession, page: int = Query(1, g=1), valid_token=Depends(validate_token)):

    if (res := check_token_response(valid_token)):
        return res

    # STATUS UPDATE -------------------------

    if request_data.status_update in ["A", "I", "DELETE"] and len(request_data.checkbox_val) > 0:
        return status_update(request_data, db, SmsTemplate)

    # SORTING, SEARCHING AND PAGINATION -------------------------

    query = db.query(SmsTemplate)
    response_data = sort_search_paginate_data(
        request_data, db, SmsTemplate, query, page, search_column="template_name")

    return JSONResponse(content=response_data, status_code=200)


@router.post("/sms-template-save")
async def add_sms_template(
    request_data: Annotated[SMSTemplateSchema, Depends(SMSTemplateSchema.from_request)],
    db: DBSession,
    valid_token=Depends(validate_token)
):
    if (res := check_token_response(valid_token)):
        return res

    return await handleSMSTemplate(request_data, db)


@router.get("/sms-template-list/edit/{edit_id}")
def sms_template_edit_data(edit_id: int, db: DBSession, valid_token=Depends(validate_token)):

    if (res := check_token_response(valid_token)):
        return res

    return edit_data(db, SmsTemplate, edit_id)
