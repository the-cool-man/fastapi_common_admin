from typing import Union
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
import models
from db_connection.session import engine
from api.v1.endpoints import admin_role_route, user_route, staff_route, site_setting_route
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path


app = FastAPI(
    docs_url=False
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

UPLOAD_DIR = Path(__file__).parent / "uploads"
app.mount("/api/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

models.Base.metadata.create_all(bind=engine)


@app.get("/debug-files")
async def debug_files():
    import os
    import json

    debug_info = {
        "current_directory": os.getcwd(),
        "uploads_exists": os.path.exists("uploads"),
        "logos_exists": os.path.exists("uploads/logos"),
        "files_in_logos": []
    }

    if os.path.exists("uploads/logos"):
        debug_info["files_in_logos"] = os.listdir("uploads/logos")

    return debug_info


# ------------------ CENTRALIZED VALIDATION ---------------------------#

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    first_error = errors[0]
    # print("first_error", first_error)
    loc = first_error.get("loc", ())
    type = first_error.get("type")
    if type == "missing":
        field = loc[-1]
        message = f"{field} is required"
    else:
        message = first_error.get("msg", "Validation error")

    return JSONResponse(
        status_code=200,
        content={
            "status": "error",
            "message": f"{message}"
        }
    )


@app.exception_handler(ValidationError)
async def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
    errors = exc.errors()
    first_error = errors[0]
    # print("first_error", first_error)
    loc = first_error.get("loc", ())
    type = first_error.get("type")
    if type == "missing":
        field = loc[-1]
        message = f"{field} is required"
    else:
        message = first_error.get("msg", "Validation error")
        if "," in message:
            message = message.split(",", 1)[-1].strip()
        else:
            pass

    return JSONResponse(
        status_code=200,
        content={
            "status": "error",
            "message": f"{message}"
        }
    )


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    print("ValueError Handler", str(exc))
    return JSONResponse(
        status_code=200,
        content={
            "status": "error",
            "message": str(exc)
        }
    )

# --------------------- ROUTES INCLUDED -------------------------#

app.include_router(admin_role_route.router)
app.include_router(user_route.router)
app.include_router(staff_route.router, prefix='/api', tags=['api'])
app.include_router(site_setting_route.router, prefix='/api', tags=['api'])


@app.get("/")
def get_role():
    return JSONResponse(content={"status": "success", "message": "Welcome Fast API URL!"}, status_code=200)
