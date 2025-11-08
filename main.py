from typing import Union
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from src import engine, user_route, staff_route, site_setting_route, models, master_route, users_content_route, template_route
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from src import set_request


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
print("UPLOAD_DIR", UPLOAD_DIR)
models.Base.metadata.create_all(bind=engine)


# @app.get("/debug-files")
# async def debug_files():
#     import os
#     import json

#     debug_info = {
#         "current_directory": os.getcwd(),
#         "uploads_exists": os.path.exists("uploads"),
#         "logos_exists": os.path.exists("uploads/logos"),
#         "files_in_logos": []
#     }

#     if os.path.exists("uploads/logos"):
#         debug_info["files_in_logos"] = os.listdir("uploads/logos")

#     return debug_info


# ------------------ CENTRALIZED VALIDATION ---------------------------#

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    first_error = errors[0]
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
    return JSONResponse(
        status_code=200,
        content={
            "status": "error",
            "message": str(exc)
        }
    )


# ------------------------MIDDLEWARE --------------------------- #

@app.middleware("http")
async def add_request_to_context(request: Request, call_next):
    set_request(request)
    response = await call_next(request)
    return response

# --------------------- ROUTES INCLUDED -------------------------#

app.include_router(user_route.router)
app.include_router(staff_route.router, prefix='/api', tags=['api'])
app.include_router(site_setting_route.router, prefix='/api', tags=['api'])
app.include_router(master_route.router, prefix='/api', tags=['api'])
app.include_router(users_content_route.router, prefix='/api', tags=['api'])
app.include_router(template_route.router, prefix='/api', tags=['api'])


@app.get("/")
def get_role():
    return JSONResponse(content={"status": "success", "message": "Welcome Fast API URL!"}, status_code=200)
