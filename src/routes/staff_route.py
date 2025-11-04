from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from typing import Annotated

from sqlalchemy import desc, asc
from ..db_connection import DBSession
from ..utils import validate_token, status_update, sort_search_paginate_data, bcrypt_context, edit_data, check_token_response
from ..models import AdminUser as Users, AdminRole as Role
from ..schemas import StaffAddSchema, ListDataSchema, StaffRoleSchema


router = APIRouter()


@router.post("/staff-save")
def staff_save(
    request_data: Annotated[StaffAddSchema, Depends(StaffAddSchema.from_request)],
    db: DBSession,
    valid_token=Depends(validate_token)
):
    if (res := check_token_response(valid_token)):
        return res

    if request_data.id is None:
        if db.query(Users).filter(
                Users.email == request_data.email).first():
            return JSONResponse(
                content={"status": "error",
                         "message": "email has already been taken."},
                status_code=200
            )
    elif request_data.id:
        if db.query(Users).filter(
                Users.id == request_data.id).first() is None:
            return JSONResponse(
                content={"status": "error",
                         "message": "Record Is not found For update."},
                status_code=200
            )
        if db.query(Users).filter(
                Users.email == request_data.email, Users.id != request_data.id).first():
            return JSONResponse(
                content={"status": "error",
                         "message": "email has already been taken."},
                status_code=200
            )

    try:
        add_staff = Users(
            id=getattr(request_data, 'id', None),
            email=request_data.email,
            password=bcrypt_context.hash(request_data.password),
            username=request_data.username,
            status=request_data.status,
            role=request_data.role,
            user_type=request_data.user_type
        )
        db.merge(add_staff)
        db.commit()

        return JSONResponse(
            content={"status": "success",
                     "message": f"Data {'inserted' if request_data.id is None else 'updated'} successfully!"},
            status_code=200
        )

    except Exception as err:
        return JSONResponse(
            content={"status": "success",
                     "message": str(err)},
            status_code=200
        )


@router.post("/staff-member-list")
def staff_member_list(request_data: Annotated[ListDataSchema, Depends(ListDataSchema.from_request)], db: DBSession, page: int = Query(1, ge=1), valid_token=Depends(validate_token)):

    if (res := check_token_response(valid_token)):
        return res

    # STATUS UPDATE -------------------------

    if request_data.status_update in ['A', 'I', 'DELETE'] and len(request_data.checkbox_val) > 0:
        return status_update(request_data, db, Users)

    # SORTING, SEARCHING AND PAGINATION -------------------------

    query = db.query(Users).filter(Users.user_type != "S")
    # query = db.query(Users).filter()
    response_data = sort_search_paginate_data(
        request_data, db, Users, query, page, search_column="username")

    return JSONResponse(content=response_data, status_code=200)


@router.get("/staff-member-list/edit/{edit_id}")
def staff_member_edit(edit_id: int, db: DBSession, valid_token=Depends(validate_token)):
    if (res := check_token_response(valid_token)):
        return res

    edit_user = edit_data(db, Users, edit_id)
    if edit_user is None:
        return JSONResponse(
            content={"status": "error", "message": "User not found!"},
            status_code=200
        )

    return JSONResponse(
        content={"status": "success", "message": "Data Display",
                 "data": edit_user.as_dict()},
        status_code=200
    )


# STAFF ROLE ROUTE -------------------------

@router.post("/staff-role-save")
def staff_role_save(
    request_data: Annotated[StaffRoleSchema, Depends(StaffRoleSchema.from_request)],
    db: DBSession,
    valid_token=Depends(validate_token)
):
    if res := check_token_response(valid_token):
        return res

    query = db.query(Role)

    try:
        check_status = [
            "role_name", "status", "site_setting", "banner", "category",
            "currency", "tax_data", "country", "state", "city",
            "media_gallery", "all_user", "chat", "rating", "site_content",
            "email_template", "sms_template", "rest_api", "payment_plan"
        ]

        if request_data.id:
            existing_role = query.filter(Role.id == request_data.id).first()
            if not existing_role:
                return JSONResponse(
                    content={"status": "error",
                             "message": "Record not found for update."},
                    status_code=200
                )

            if query.filter(Role.role_name == request_data.role_name, Role.id != request_data.id).first():
                return JSONResponse(
                    content={"status": "error",
                             "message": "role_name has already been taken."},
                    status_code=200
                )

            for field in check_status:
                setattr(existing_role, field, getattr(request_data, field))

            db.commit()
            db.refresh(existing_role)

            return JSONResponse(
                content={"status": "success",
                         "message": "Role updated successfully."},
                status_code=200
            )
        if query.filter(Role.role_name == request_data.role_name).first():
            return JSONResponse(
                content={"status": "error",
                         "message": "role_name has already been taken."},
                status_code=200
            )

        role_data = {field: getattr(request_data, field)
                     for field in check_status}
        add_role = Role(**role_data)

        db.add(add_role)
        db.commit()
        db.refresh(add_role)

        return JSONResponse(
            content={"status": "success",
                     "message": "Role inserted successfully."},
            status_code=200
        )

    except Exception as err:
        db.rollback()
        return JSONResponse(
            content={"status": "error", "message": str(err)},
            status_code=500
        )


@router.post("/staff-role-list")
def staff_role_list(request_data: Annotated[ListDataSchema, Depends(ListDataSchema.from_request)], db: DBSession, page: int = Query(1, ge=1), valid_token=Depends(validate_token)):

    if (res := check_token_response(valid_token)):
        return res

    # STATUS UPDATE -------------------------

    if request_data.status_update in ['A', 'I', 'DELETE'] and len(request_data.checkbox_val) > 0:
        return status_update(request_data, db, Role)

    # SORTING, SEARCHING AND PAGINATION -------------------------

    query = db.query(Role).filter()
    response_data = sort_search_paginate_data(
        request_data, db, Role, query, page, search_column="role_name")

    return JSONResponse(content=response_data, status_code=200)


@router.get("/staff-role-list/edit/{edit_id}")
def staff_role_edit(edit_id: int, db: DBSession, valid_token=Depends(validate_token)):
    if (res := check_token_response(valid_token)):
        return res

    edit_user = edit_data(db, Role, edit_id)
    if edit_user is None:
        return JSONResponse(
            content={"status": "error", "message": "User not found!"},
            status_code=200
        )

    return JSONResponse(
        content={"status": "success", "message": "Data Display",
                 "data": edit_user.as_dict()},
        status_code=200
    )
