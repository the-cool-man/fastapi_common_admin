from fastapi import Request
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from ..db_connection import DBSession
from ..utils import bcrypt_context, get_jwt_token, validate_token
from ..models import AdminUser as Users, AdminRole
from ..schemas import LoginSchema, ChangePassword
from typing import Annotated

router = APIRouter(
    prefix='/api',
    tags=['api']
)


# ----------------- LOGIN ROUTE --------------------------#

@router.post("/login")
async def login_user(
    request: Request,
    db: DBSession,
    request_data: LoginSchema = Depends(LoginSchema.from_request)
):
    try:
        user = db.query(Users).filter(
            Users.email == request_data.email).first()

        if user is None or not bcrypt_context.verify(request_data.password, user.password):
            return JSONResponse(
                content={"status": "error",
                         "message": "Email or password is wrong"},
                status_code=200
            )

        role_data = db.query(AdminRole).filter(
            AdminRole.id == user.role).first()
        role_name = role_data.role_name if role_data else "User"

        JWToken = get_jwt_token(request, user.email, user.id, role_name)

        return JSONResponse(
            content={
                "status": "success",
                "message": "Login Successfully!",
                "userdata": user.as_dict(),
                "roledata": role_data.as_dict(),
                "jwt": JWToken,
            },
            status_code=200
        )

    except Exception as error:
        return JSONResponse(content={"status": "error", "message": str(error)}, status_code=200)


@router.post("/change-password")
async def change_password(request_data: Annotated[ChangePassword, Depends(ChangePassword.from_request)], db: DBSession, valid_token=Depends(validate_token)):

    if isinstance(valid_token, JSONResponse):
        return valid_token

    try:
        user = db.query(Users).filter(Users.id == request_data.id).first()

        if user is None:
            return JSONResponse(content={"status": "error",
                                         "message": "Record Not found!"})

        if not bcrypt_context.verify(request_data.password, user.password):
            return JSONResponse(content={"status": "error",
                                         "message": "Please enter a valid old password!"})

        hash_new_password = bcrypt_context.hash(request_data.new_password)
        user.password = hash_new_password
        db.commit()
        return JSONResponse(content={"status": "success",
                                     "message": "Password changed successfully!"})

    except Exception as err:
        return JSONResponse(content={"status": "error",
                                     "message": str(err)})
