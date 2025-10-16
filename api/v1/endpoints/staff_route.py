from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from typing import Annotated

from sqlalchemy import desc, asc
from db_connection import DBSession
from utils import validate_token, bcrypt_context
from models import AdminUser as Users
from schemas import StaffAddSchema, StaffListSchema


router = APIRouter()


@router.post("/staff-save")
def staff_save(
    request_data: Annotated[StaffAddSchema, Depends(StaffAddSchema.from_request)],
    db: DBSession,
    valid_user=Depends(validate_token)
):
    if isinstance(valid_user, JSONResponse):
        return valid_user

    if request_data.id is None:
        is_exist = db.query(Users).filter(
            Users.email == request_data.email).first()

        if is_exist:
            return JSONResponse(
                content={"status": "error",
                         "message": "The email has already been taken."},
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
def staff_member_list(request_data: Annotated[StaffListSchema, Depends(StaffListSchema.from_request)], db: DBSession, page: int = Query(1, ge=1), valid_user=Depends(validate_token)):

    if isinstance(valid_user, JSONResponse):
        return valid_user
    if request_data.status_update in ['A', 'I'] and len(request_data.checkbox_val) > 0:
        try:
            rows_updated = db.query(Users).filter(
                Users.user_type != "S" and Users.id.in_(
                    request_data.checkbox_val)
            ).update(
                {Users.status: request_data.status_update},
                synchronize_session=False
            )
            db.commit()
            if rows_updated == 0:
                return JSONResponse(
                    content={"status": "error",
                             "message": "No users found to update."},
                    status_code=200
                )
            return JSONResponse(
                content={"status": "success",
                         "message": "Status updated successfully!"},
                status_code=200
            )

        except Exception as err:
            db.rollback()
            return JSONResponse(
                content={"status": "error", "message": str(err)},
                status_code=200
            )

    query = db.query(Users).filter(Users.user_type != "S")
    if request_data.search_field:
        search_value = f"%{request_data.search_field}%"
        query = query.filter(
            Users.username.ilike(
                search_value) | Users.email.ilike(search_value)
        )

    sort_column = getattr(Users, request_data.sort_column)
    if request_data.sort_order.upper() == "ASC":
        query = query.order_by(asc(sort_column))
    else:
        query = query.order_by(desc(sort_column))

    approve_count = db.query(Users).filter(
        Users.user_type != "S" and Users.status == "A").count()

    unapprove_count = db.query(Users).filter(
        Users.user_type != "S" and Users.status == "I").count()

    limit = request_data.limit_per_page
    offset = (page - 1) * limit

    staff_members = query.offset(offset).limit(limit).all()

    staff_member_list = [member.as_dict()
                         for member in staff_members] if staff_members else []

    response_data = {
        "status": "success",
        "message": "Staff member list",

        "data": {
            "data": staff_member_list
        }
    }

    if staff_member_list:
        response_data["data"].update({
            "total": approve_count + unapprove_count,
            "current_page": page,
            "per_page": limit
        })
        response_data.update({"approve_count": approve_count,
                              "unapprove_count": unapprove_count, })

    return JSONResponse(content=response_data, status_code=200)


@router.get("/staff-member-list/edit/{edit_id}")
def staff_member_edit(edit_id: int, db: DBSession, valid_user=Depends(validate_token)):
    if isinstance(valid_user, JSONResponse):
        return valid_user

    edit_user = db.query(Users).filter(Users.id == edit_id).first()
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
