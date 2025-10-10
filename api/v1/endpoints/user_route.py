from fastapi.exceptions import RequestValidationError
from fastapi import FastAPI, Request
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import JSONResponse
from typing import Annotated
from utils import DBSession
from utils import validate_token, bcrypt_context, get_jwt_token
from models import AdminUser as Users, AdminRole
from schemas import LoginForm, StaffRequest

router = APIRouter(
    prefix='/api',
    tags=['api']
)


# ----------------- LOGIN ROUTE --------------------------#

@router.post("/login")
async def login_user(
    request: Request,
    db: DBSession,
    request_data: LoginForm = Depends(LoginForm.as_form)
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


# ----------------- STAFF ROUTE --------------------------#

@router.post("/staff-save")
def staff_save(
    request_data: Annotated[StaffRequest, Depends()],
    db: DBSession,
    user=Depends(validate_token)
):
    if isinstance(user, JSONResponse):
        return user

    is_exist = db.query(Users).filter(
        Users.email == request_data.email).first()

    if is_exist:
        return JSONResponse(
            content={"status": "error",
                     "message": "Email Already Exist!"},
            status_code=200
        )

    try:
        add_staff = Users(
            email=request_data.email,
            password=bcrypt_context.hash(request_data.password),
            username=request_data.username,
            status=request_data.status,
            role=request_data.role,
            user_type=request_data.user_type
        )
        db.add(add_staff)
        db.commit()

        return JSONResponse(
            content={"status": "success",
                     "message": "Staff Save Successfully!"},
            status_code=200
        )

    except Exception as err:
        return JSONResponse(
            content={"status": "success",
                     "message": str(err)},
            status_code=200
        )
