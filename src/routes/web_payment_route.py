from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse
from typing import Annotated
from ..schemas import ListDataSchema
from ..utils import check_token_response, status_update, sort_search_paginate_data, validate_token, edit_data
from ..models import WebServiceModel as WebService, UserPaymentModel as UserPayment
from ..db_connection import DBSession
from ..schemas import MembershipPlanSchema, WebServiceSchema, CouponSchema
from ..controllers import handleWebServiceSave, handleMembershipPlanSave, handleCouponSave

router = APIRouter()



# WEB SERVICE ROUTE --------------------------

@router.post("/web-service-save")
async def web_service_save_data(
    request_data: Annotated[WebServiceSchema, Depends(WebServiceSchema.from_request)],
    db: DBSession,
    valid_token=Depends(validate_token)
):
    if res := check_token_response(valid_token):
        return res

    return await handleWebServiceSave(request_data, db)


@router.post("/web-service-list")
def web_service_get_data(request_data: Annotated[ListDataSchema, Depends(ListDataSchema.from_request)], db: DBSession, page: int = Query(1, g=1), valid_token=Depends(validate_token)):

    if (res := check_token_response(valid_token)):
        return res

    # STATUS UPDATE -------------------------

    if request_data.status_update in ["A", "I", "DELETE"] and len(request_data.checkbox_val) > 0:
        return status_update(request_data, db, WebService)

    # SORTING, SEARCHING AND PAGINATION -------------------------

    query = db.query(WebService)
    response_data = sort_search_paginate_data(
        request_data, db, WebService, query, page, search_column="service_name")

    return JSONResponse(content=response_data, status_code=200)


@router.get("/web-service-list/edit/{edit_id}")
def web_service_edit_data(edit_id: int, db: DBSession, valid_token=Depends(validate_token)):

    if (res := check_token_response(valid_token)):
        return res

    return edit_data(db, WebService, edit_id)


# MEMBERSHIP ROUTE --------------------------

@router.post("/membership-plan-save")
async def membership_save_data(
    request_data: Annotated[MembershipPlanSchema, Depends(MembershipPlanSchema.from_request)],
    db: DBSession,
    valid_token=Depends(validate_token)
):
    if res := check_token_response(valid_token):
        return res

    return await handleMembershipPlanSave(request_data, db)


@router.post("/membership-plan-list")
def membership_get_data(request_data: Annotated[ListDataSchema, Depends(ListDataSchema.from_request)], db: DBSession, page: int = Query(1, g=1), valid_token=Depends(validate_token)):

    if (res := check_token_response(valid_token)):
        return res

    # STATUS UPDATE -------------------------

    if request_data.status_update in ["A", "I", "DELETE"] and len(request_data.checkbox_val) > 0:
        return status_update(request_data, db, UserPayment)

    # SORTING, SEARCHING AND PAGINATION -------------------------

    query = db.query(UserPayment)
    response_data = sort_search_paginate_data(
        request_data, db, UserPayment, query, page, search_column="plan_name")

    return JSONResponse(content=response_data, status_code=200)


@router.get("/membership-plan-list/edit/{edit_id}")
def membership_edit_data(edit_id: int, db: DBSession, valid_token=Depends(validate_token)):

    if (res := check_token_response(valid_token)):
        return res

    return edit_data(db, UserPayment, edit_id)


# COUPON ROUTE --------------------------

@router.post("/coupon-save")
async def coupon_save_data(
    request_data: Annotated[CouponSchema, Depends(CouponSchema.from_request)],
    db: DBSession,
    valid_token=Depends(validate_token)
):
    if res := check_token_response(valid_token):
        return res

    return await handleCouponSave(request_data, db)


@router.post("/coupon-list")
def coupon_get_data(request_data: Annotated[ListDataSchema, Depends(ListDataSchema.from_request)], db: DBSession, page: int = Query(1, g=1), valid_token=Depends(validate_token)):

    if (res := check_token_response(valid_token)):
        return res

    # STATUS UPDATE -------------------------

    if request_data.status_update in ["A", "I", "DELETE"] and len(request_data.checkbox_val) > 0:
        return status_update(request_data, db, UserPayment)

    # SORTING, SEARCHING AND PAGINATION -------------------------

    query = db.query(UserPayment)
    response_data = sort_search_paginate_data(
        request_data, db, UserPayment, query, page, search_column="coupon_code")

    return JSONResponse(content=response_data, status_code=200)


@router.get("/coupon-list/edit/{edit_id}")
def coupon_edit_data(edit_id: int, db: DBSession, valid_token=Depends(validate_token)):

    if (res := check_token_response(valid_token)):
        return res

    return edit_data(db, UserPayment, edit_id)

