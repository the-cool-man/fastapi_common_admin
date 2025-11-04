from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from typing import Annotated
from ..schemas import ListDataSchema
from ..utils import check_token_response, status_update, sort_search_paginate_data, validate_token, edit_data
from ..models import OrdinaryUserModel as OrdinaryUser, OrdinaryUserDetailModel as OrdinaryUserDetail
from ..db_connection import DBSession
from ..schemas import OrdinaryUserSchema
from ..controllers import handleUserContentSave

router = APIRouter()


# ORDINARY USERS ROUTE ----------------------------

@router.post("/user-data-list")
def city_get_data(request_data: Annotated[ListDataSchema, Depends(ListDataSchema.from_request)], db: DBSession, page: int = Query(1, g=1), valid_token=Depends(validate_token)):

    if (res := check_token_response(valid_token)):
        return res

    # STATUS UPDATE -------------------------

    if request_data.status_update in ["A", "I", "DELETE"] and len(request_data.checkbox_val) > 0:
        return status_update(request_data, db, OrdinaryUser)

    # SORTING, SEARCHING AND PAGINATION -------------------------

    query = db.query(OrdinaryUser)
    response_data = sort_search_paginate_data(
        request_data, db, OrdinaryUser, query, page, search_column="name")

    return JSONResponse(content=response_data, status_code=200)


@router.post("/user-data-save")
async def user_save_data(
    request_data: Annotated[OrdinaryUserSchema, Depends(OrdinaryUserSchema.from_request)],
    db: DBSession,
    valid_token=Depends(validate_token)
):
    if (res := check_token_response(valid_token)):
        return res

    return await handleUserContentSave(request_data, db)


# @router.get("/city-list/edit/{edit_id}")
# def city_edit_data(edit_id: int, db: DBSession, valid_token=Depends(validate_token)):

#     if (res := check_token_response(valid_token)):
#         return res

#     edit_social_data = edit_data(db, OrdinaryUser, edit_id)

#     if edit_social_data is None:
#         return JSONResponse(
#             content={"status": "error", "message": "Record not found!"},
#             status_code=200
#         )

#     return JSONResponse(
#         content={"status": "success", "message": "Data Display!",
#                  "data": edit_social_data.as_dict()},
#         status_code=200
#     )
