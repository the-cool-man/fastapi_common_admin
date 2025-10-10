from typing import Union
from fastapi import FastAPI, Request
import models
from db_connection.session import engine
from api.v1.endpoints import admin_role_route, user_route
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError


app = FastAPI(
    prefix='/api',
    tags='api',
    docs_url=False
)

models.Base.metadata.create_all(bind=engine)

# ------------------ CENTRALIZED VALIDATION ---------------------------#


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_msg = exc.errors()[0]['msg']
    field = exc.errors()[0]['loc'][-1]

    return JSONResponse(
        status_code=200,
        content={
            "status": "error",
            "message": f"{field} Field Is required"
        }
    )


@app.exception_handler(ValidationError)
async def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
    error_msg = exc.errors()[0]['msg']
    field = exc.errors()[0]['loc'][-1]

    return JSONResponse(
        status_code=200,
        content={
            "status": "error",
            "message": f"{error_msg}"
        }
    )


# --------------------- ROUTES INCLUDED -------------------------#

app.include_router(admin_role_route.router)
app.include_router(
    user_route.router,
)


@app.get("/")
def get_role():
    return JSONResponse(content={"status": "success", "message": "Welcome Fast API URL!"}, status_code=200)
