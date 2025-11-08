from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse
from typing import Annotated
from ..schemas import ListDataSchema
from ..utils import check_token_response, status_update, sort_search_paginate_data, validate_token, edit_data
from ..models import OrdinaryUserModel as OrdinaryUser, MediaGalleryModel as MediaGallery, CmsPageModel as CmsPage
from ..db_connection import DBSession
from ..schemas import OrdinaryUserSchema, MediaGallerySchema, CmsPageSchema
from ..controllers import handleUserContentSave, handleGallerySave, handleCmsPageSave
import os
import uuid
import time


router = APIRouter()
CMS_IMG_DIR = os.path.join("uploads", "cmsImg")


# ORDINARY USERS ROUTE ----------------------------

@router.post("/user-data-list")
def user_get_data(request_data: Annotated[ListDataSchema, Depends(ListDataSchema.from_request)], db: DBSession, page: int = Query(1, g=1), valid_token=Depends(validate_token)):

    if (res := check_token_response(valid_token)):
        return res

    # STATUS UPDATE -------------------------

    if request_data.status_update in ["A", "I", "DELETE"] and len(request_data.checkbox_val) > 0:
        return status_update(request_data, db, OrdinaryUser)

    # SORTING, SEARCHING AND PAGINATION -------------------------

    query = db.query(OrdinaryUser)
    response_data = sort_search_paginate_data(
        request_data, db, OrdinaryUser, query, page, search_column="name")

    return JSONResponse(content=response_data, status_code=200)


@router.post("/user-data-save")
async def user_save_data(
    request_data: Annotated[OrdinaryUserSchema, Depends(OrdinaryUserSchema.from_request)],
    db: DBSession,
    valid_token=Depends(validate_token)
):
    if (res := check_token_response(valid_token)):
        return res

    return await handleUserContentSave(request_data, db)


# PHOTO GALLERY ROUTE ----------------------------

@router.post("/photo-gallery-save")
async def gallery_save_data(
    request_data: Annotated[MediaGallerySchema, Depends(MediaGallerySchema.from_request)],
    db: DBSession,
    valid_token=Depends(validate_token)
):
    if (res := check_token_response(valid_token)):
        return res

    return await handleGallerySave(request_data, db)


@router.post("/photo-gallery-data-list")
def gallery_get_data(request_data: Annotated[ListDataSchema, Depends(ListDataSchema.from_request)], db: DBSession, page: int = Query(1, g=1), valid_token=Depends(validate_token)):

    if (res := check_token_response(valid_token)):
        return res

    # STATUS UPDATE -------------------------

    if request_data.status_update in ["A", "I", "DELETE"] and len(request_data.checkbox_val) > 0:
        return status_update(request_data, db, MediaGallery)

    # SORTING, SEARCHING AND PAGINATION -------------------------

    query = db.query(MediaGallery)
    response_data = sort_search_paginate_data(
        request_data, db, MediaGallery, query, page, search_column="created_at", folder="gallery")

    return JSONResponse(content=response_data, status_code=200)


@router.get("/photo-gallery-data-list/edit/{edit_id}")
def gallery_edit_data(edit_id: int, db: DBSession, valid_token=Depends(validate_token)):

    if (res := check_token_response(valid_token)):
        return res

    edit_social_data = edit_data(db, MediaGallery, edit_id, folder="gallery")


# CMS PAGES ROUTE --------------------------

@router.post("/cms-save")
async def cms_save_data(
    request_data: Annotated[CmsPageSchema, Depends(CmsPageSchema.from_request)],
    db: DBSession,
    valid_token=Depends(validate_token)
):
    if res := check_token_response(valid_token):
        return res

    return await handleCmsPageSave(request_data, db)


@router.post("/cms-list-data")
def cms_get_data(request_data: Annotated[ListDataSchema, Depends(ListDataSchema.from_request)], db: DBSession, page: int = Query(1, g=1), valid_token=Depends(validate_token)):

    if (res := check_token_response(valid_token)):
        return res

    # STATUS UPDATE -------------------------

    if request_data.status_update in ["A", "I", "DELETE"] and len(request_data.checkbox_val) > 0:
        return status_update(request_data, db, CmsPage)

    # SORTING, SEARCHING AND PAGINATION -------------------------

    query = db.query(CmsPage)
    response_data = sort_search_paginate_data(
        request_data, db, CmsPage, query, page, search_column="meta_title", folder="cmsImg")

    return JSONResponse(content=response_data, status_code=200)


@router.get("/cms-list-data/edit/{edit_id}")
def cms_edit_data(edit_id: int, db: DBSession, valid_token=Depends(validate_token)):

    if (res := check_token_response(valid_token)):
        return res

    return edit_data(db, CmsPage, edit_id, folder="cmsImg")
