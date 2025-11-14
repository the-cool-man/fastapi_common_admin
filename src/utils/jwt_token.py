from datetime import timedelta, datetime
from jose import jwt, JWTError, ExpiredSignatureError
from typing import Annotated
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from ..models import AdminUser as Users
import hashlib
import uuid
import os
from dotenv import load_dotenv
load_dotenv()


# SECRET_KEY = "alfa@123"
# ALGORITHM = 'HS256'
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/login", auto_error=False)
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


# ----------- ROLE AND IP HASHING -------------#
def get_role_hash(role: str) -> str:
    """Return a consistent hash for a user role."""
    return hashlib.md5(role.encode()).hexdigest()


def get_ip_hash(ip: str) -> str:
    """Return a hash of the user's IP address."""
    return hashlib.md5(ip.encode()).hexdigest()


# ---------- CREATE AND GET JWToken ---------------#

def get_jwt_token(request: Request, email: str, user_id: int, role: str):
    now = datetime.utcnow()
    expires = now + timedelta(seconds=30)

    iss = str(request.base_url) + "api/login"

    payload = {
        "iss": iss,
        "iat": now,
        "nbf": now,
        # "exp": expires,
        "env": os.getenv("APP_ENV"),
        "jti": str(uuid.uuid4())[:16],
        "sub": str(user_id),

        "prv": str(uuid.uuid4()),
        "user_id": user_id,
        "email": email,
        "ipa": get_ip_hash(request.client.host),
        "ura": get_role_hash(role),
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


# ------------- VALIDATE JWToken ----------------#
async def validate_token(token: str = Depends(oauth2_bearer)):
    try:
        if not token:
            return JSONResponse(
                content={"status": "error",
                         "message": "Token Is Not Provided!"},
                status_code=401
            )

        payload = jwt.decode(token, SECRET_KEY, algorithms=[
                             ALGORITHM],
                             options={
            "verify_nbf": False,

        })

        current_env = os.getenv("APP_ENV")
        token_env = payload.get("env")
        email = payload.get('email')
        user_id = payload.get('user_id')

        if token_env != current_env:
            return JSONResponse(
                content={"status": "error",
                         "message": "Token Is Invalid!"},
                status_code=401
            )

        if email is None or user_id is None:
            return JSONResponse(
                content={"status": "error", "message": "Token Is Invalid!"},
                status_code=401
            )

        return {"email": email, "user_id": user_id}

    except ExpiredSignatureError:
        return JSONResponse(
            content={"status": "error", "message": "Token Expired!"},
            status_code=401
        )

    except JWTError as error:
        return JSONResponse(
            content={"status": "error",
                     "message": str(error) or "Token Is Invalid"},
            status_code=401
        )
