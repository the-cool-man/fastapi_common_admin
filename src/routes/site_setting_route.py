from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from ..models import SiteConfig
from ..schemas import LogoFavSchema, CommonSetting, EmailUpdate
from ..db_connection import DBSession
from ..utils import validate_token
import os
import time
from pathlib import Path
from zoneinfo import available_timezones
import json
import uuid


router = APIRouter()


UPLOAD_DIR = "uploads"
LOGO_DIR = os.path.join(UPLOAD_DIR, "logos")
FAVICON_DIR = os.path.join(UPLOAD_DIR, "favicons")


async def handleLogoFavicon(request_data, db):
    logo_filename = None
    favicon_filename = None
    logo_path = None
    favicon_path = None
    print("request_data.logo", request_data.logo)
    try:
        if getattr(request_data, "id", None):
            site_config = db.query(SiteConfig).filter(
                SiteConfig.id == request_data.id).first()
            if not site_config:
                return {"status": "error", "message": "Record Not Found"}
            message = "updated"
        else:
            site_config = SiteConfig()
            db.add(site_config)
            message = "inserted"

        if request_data.logo:
            if site_config.logo:
                old_logo_path = os.path.join(LOGO_DIR, site_config.logo)
                if os.path.exists(old_logo_path):
                    os.remove(old_logo_path)

            fileName = request_data.logo.filename
            ext = os.path.splitext(fileName)[1]
            unique_str = f"{int(time.time())}{uuid.uuid4().hex[:10]}"
            logo_filename = f"{unique_str}{ext}"
            logo_path = os.path.join(LOGO_DIR, logo_filename)

            with open(logo_path, "wb") as bufferFile:
                bufferFile.write(await request_data.logo.read())

            site_config.logo = logo_filename

        if request_data.favicon:
            if site_config.favicon:
                old_favicon_path = os.path.join(
                    FAVICON_DIR, site_config.favicon)
                if os.path.exists(old_favicon_path):
                    os.remove(old_favicon_path)

            fileName = request_data.favicon.filename
            ext = os.path.splitext(fileName)[1]
            unique_str = f"{int(time.time())}{uuid.uuid4().hex[:10]}"
            favicon_filename = f"{unique_str}{ext}"
            favicon_path = os.path.join(FAVICON_DIR, favicon_filename)
            with open(favicon_path, "wb") as bufferFile:
                bufferFile.write(await request_data.favicon.read())

            site_config.favicon = favicon_filename

        db.commit()
        db.refresh(site_config)

        return {"status": "success", "message": f"Data {message} successfully"}

    except Exception as e:
        db.rollback()
        # Cleanup newly uploaded files if DB operation fails
        if logo_path and os.path.exists(logo_path):
            os.remove(logo_path)
        if favicon_path and os.path.exists(favicon_path):
            os.remove(favicon_path)
        return {"status": "error", "message": f"DB Error: {str(e)}"}


async def handleCommonSetting(request_data, db):
    try:
        if getattr(request_data, "id", None):
            site_config = db.query(SiteConfig).filter(
                SiteConfig.id == request_data.id).first()
            if not site_config:
                return {"status": "error", "message": "Record Not Found"}
            message = "updated"
        else:
            site_config = SiteConfig()
            db.add(site_config)   # add new object to session
            message = "inserted"

        for field in [
            "contact_no", "google_analytics_code", "footer_text", "about_footer",
            "full_address", "web_name", "web_frienly_name", "website_title",
            "website_description", "website_keywords", "map_address", "timezone"
        ]:
            value = getattr(request_data, field, None)
            if value is not None:
                setattr(site_config, field, value)

        db.commit()
        db.refresh(site_config)

        return {"status": "success", "message": f"Data {message} successfully"}
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": f"DB Error: {str(e)}"}


async def handleEmailSetting(request_data, db):
    try:
        if getattr(request_data, 'id', None):
            site_config = db.query(SiteConfig).filter(
                SiteConfig.id == request_data.id).first()
            if site_config is None:
                return {"status": "error", "message": "Record Not Found"}
            message = "Updated"

        else:
            site_config = SiteConfig()
            db.add(site_config)
            message = "Inserted"

        site_config.from_email = request_data.from_email
        site_config.contact_email = request_data.contact_email

        db.commit()
        # db.refresh(site_config)
        return {"status": "success", "message": f"Data {message} Successfully"}

    except Exception as err:
        return {"status": "error", "message": str(err)}


TIME_ZONE = Path(__file__).parent.parent / "utils" / "timezone.json"


def getTimeZoneData():
    print(TIME_ZONE)

    with open(TIME_ZONE, "r", encoding="utf-8") as file:
        data = json.load(file)  # <- remove 'await'
    return data


@router.post("/basic-site-setting")
async def basic_site_setting(
    logo_fav_data: Annotated[LogoFavSchema, Depends(LogoFavSchema.from_request)],
    common_setting: Annotated[CommonSetting, Depends(CommonSetting.from_request)],
    email_update: Annotated[EmailUpdate, Depends(EmailUpdate.from_request)],
    db: DBSession,
    valid_user=Depends(validate_token)
):
    if isinstance(valid_user, JSONResponse):
        return valid_user

    # logo and favicon handle ----------------------------
    if logo_fav_data.flag == "logo_fav":
        result = await handleLogoFavicon(logo_fav_data, db)
        return JSONResponse(
            content=result,
            status_code=200
        )
    elif common_setting.flag == "basic_setting":
        result = await handleCommonSetting(common_setting, db)
        return JSONResponse(
            content=result,
            status_code=200
        )
    elif common_setting.flag == "update_email":
        result = await handleEmailSetting(email_update, db)
        return JSONResponse(
            content=result,
            status_code=200
        )
    else:
        return JSONResponse(
            content={"status": "error", "message": "flag is not proper!"},
            status_code=200
        )


@router.get("/all_site_setting_data")
async def get_all_site_setting_data(request: Request, db: DBSession, valid_user=Depends(validate_token)):

    if isinstance(valid_user, JSONResponse):
        return valid_user

    base_url = f"{request.url.scheme}://{request.url.hostname}:{request.url.port}/api/uploads"

    try:
        # synchronous query
        result = db.query(SiteConfig).filter(SiteConfig.status == "A").first()

        if not result:
            return JSONResponse(
                content={"status": "error",
                         "message": "No site config found", "data": []},
                status_code=200
            )

        time_zone_data = getTimeZoneData()
        return JSONResponse(
            content={"status": "success",
                     "message": "All Data Display",
                     "data": result.as_dict(base_url=base_url),
                     "time_zone":  time_zone_data},
            status_code=200
        )

    except Exception as error:
        return JSONResponse(
            content={"status": "error",
                     "message": f"{str(error)}"},
            status_code=500
        )

