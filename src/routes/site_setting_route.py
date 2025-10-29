from fastapi import APIRouter, Depends, Request, Query
from fastapi.responses import JSONResponse
from typing import Annotated
from ..models import SiteConfig, SocialMedia as Social, PublicPageSEO as PageSEO
from ..schemas import LogoFavSchema, CommonSetting, EmailUpdate, ListDataSchema, SocialMediaSchema, PublicPageSEOSchema
from ..db_connection import DBSession
from ..utils import validate_token, status_update, check_token_response, sort_search_paginate_data, edit_data
from ..controllers import handleLogoFavicon, handleCommonSetting, handleEmailSetting, handleSocialMedia, handlePublicPageSEO
import os
from pathlib import Path
import json

router = APIRouter()

SOCIAL_LOGO_DIR = os.path.join("uploads", "social")
TIME_ZONE = Path(__file__).parent.parent / "utils" / "timezone.json"


def getTimeZoneData():

    with open(TIME_ZONE, "r", encoding="utf-8") as file:
        data = json.load(file)  # <- remove 'await'
    return data


@router.post("/basic-site-setting")
async def basic_site_setting(
    logo_fav_data: Annotated[LogoFavSchema, Depends(LogoFavSchema.from_request)],
    common_setting: Annotated[CommonSetting, Depends(CommonSetting.from_request)],
    email_update: Annotated[EmailUpdate, Depends(EmailUpdate.from_request)],
    db: DBSession,
    valid_token=Depends(validate_token)
):
    if isinstance(valid_token, JSONResponse):
        return valid_token

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
def get_all_site_setting_data(request: Request, db: DBSession, valid_token=Depends(validate_token)):

    if isinstance(valid_token, JSONResponse):
        return valid_token

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


# SOCIAL MEDIA ROUTE ----------------------------

@router.post("/social-media")
def get_social_media_data(request_data: Annotated[ListDataSchema, Depends(ListDataSchema.from_request)], db: DBSession, page: int = Query(1, g=1), valid_token=Depends(validate_token)):

    if (res := check_token_response(valid_token)):
        return res

    # STATUS UPDATE -------------------------

    if request_data.status_update in ["A", "I", "DELETE"] and len(request_data.checkbox_val) > 0:
        return status_update(request_data, db, Social)

    # SORTING, SEARCHING AND PAGINATION -------------------------

    query = db.query(Social)
    response_data = sort_search_paginate_data(
        request_data, db, Social, query, page)

    return JSONResponse(content=response_data, status_code=200)


@router.post("/add-social-media-link")
def add_social_media(
    request_data: Annotated[SocialMediaSchema, Depends(SocialMediaSchema.from_request)],
    db: DBSession,
    valid_token=Depends(validate_token)
):
    if (res := check_token_response(valid_token)):
        return res

    return handleSocialMedia(request_data, db)


@router.get("/social-media/edit/{edit_id}")
def social_edit_data(edit_id: int, db: DBSession, valid_token=Depends(validate_token)):

    if (res := check_token_response(valid_token)):
        return res

    edit_social_data = edit_data(db, Social, edit_id)

    if edit_social_data is None:
        return JSONResponse(
            content={"status": "error", "message": "Record not found!"},
            status_code=200
        )

    return JSONResponse(
        content={"status": "success", "message": "Data Display!",
                 "data": edit_social_data.as_dict()},
        status_code=200
    )


# PUBLIC PAGE SEO ROUTE ----------------------------

@router.post("/seo-pages-data")
def get_page_seo_data(request_data: Annotated[ListDataSchema, Depends(ListDataSchema.from_request)], db: DBSession, page: int = Query(1, g=1), valid_token=Depends(validate_token)):

    if (res := check_token_response(valid_token)):
        return res

    # STATUS UPDATE -------------------------

    if request_data.status_update in ["A", "I", "DELETE"] and len(request_data.checkbox_val) > 0:
        return status_update(request_data, db, PageSEO)

    # SORTING, SEARCHING AND PAGINATION -------------------------

    query = db.query(PageSEO)
    response_data = sort_search_paginate_data(
        request_data, db, PageSEO, query, page)

    return JSONResponse(content=response_data, status_code=200)


@router.post("/add-update-seo-page")
async def add_page_seo(
    request_data: Annotated[PublicPageSEOSchema, Depends(PublicPageSEOSchema.from_request)],
    db: DBSession,
    valid_token=Depends(validate_token)
):
    if (res := check_token_response(valid_token)):
        return res

    return await handlePublicPageSEO(request_data, db)


@router.get("/seo-edit/{edit_id}")
def page_seo_edit_data(edit_id: int, db: DBSession, valid_token=Depends(validate_token)):

    if (res := check_token_response(valid_token)):
        return res

    edit_social_data = edit_data(db, PageSEO, edit_id)

    if edit_social_data is None:
        return JSONResponse(
            content={"status": "error", "message": "Record not found!"},
            status_code=200
        )

    return JSONResponse(
        content={"status": "success", "message": "Data Display!",
                 "data": edit_social_data.as_dict()},
        status_code=200
    )
