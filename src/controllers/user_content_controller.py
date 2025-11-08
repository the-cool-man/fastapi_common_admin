
from ..utils import bcrypt_context
from ..models import OrdinaryUserModel as OrdinaryUser, OrdinaryUserDetailModel as OrdinaryUserDetail, MediaGalleryModel as MediaGallery, CmsPageModel as CmsPage
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
import os
import time
import uuid
from pathlib import Path
from datetime import datetime

UPLOAD_DIR = "uploads"
USER_DIR = os.path.join(UPLOAD_DIR, "userImg")
PHOTO_DIR = os.path.join(UPLOAD_DIR, "gallery")
CMS_IMG_DIR = os.path.join(UPLOAD_DIR, "cmsImg")


async def handle_file_upload(file, upload_dir, old_file=None):

    if old_file:
        old_path = os.path.join(upload_dir, old_file)
        if os.path.exists(old_path):
            os.remove(old_path)

    file_name = file.filename
    ext = os.path.splitext(file_name)[1]
    unique_str = f"{int(time.time())}{uuid.uuid4().hex[:10]}"
    new_filename = f"{unique_str}{ext}"
    new_path = os.path.join(upload_dir, new_filename)

    with open(new_path, "wb") as f:
        f.write(await file.read())

    return new_filename


def parse_birthdate(date_str: str):
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    raise ValueError("Invalid date format. Use YYYY-MM-DD or DD/MM/YYYY.")


async def handleUserContentSave(request_data, db):

    try:
        if request_data.id is None:
            is_name_exist = db.query(OrdinaryUser).filter(
                OrdinaryUser.name == request_data.name
            ).first()

            if is_name_exist:
                return JSONResponse(
                    content={"status": "error",
                             "message": "Name has already been taken."},
                    status_code=200
                )

            model_data = OrdinaryUser()
            message = "inserted"
        else:
            model_data = db.query(OrdinaryUser).filter(
                OrdinaryUser.id == request_data.id
            ).first()

            if not model_data:
                return JSONResponse(
                    content={"status": "error",
                             "message": "Record not found!"},
                    status_code=200
                )

            if db.query(OrdinaryUser).filter(
                OrdinaryUser.name == request_data.name,
                OrdinaryUser.id != request_data.id
            ).first():
                return JSONResponse(
                    content={"status": "error",
                             "message": "Name has already been taken."},
                    status_code=200
                )

            message = "updated"

        model_data.status = request_data.status
        model_data.name = request_data.name
        model_data.email = request_data.email
        model_data.contact_number = request_data.contact_number
        model_data.birthdate = parse_birthdate(request_data.birthdate)
        model_data.password = bcrypt_context.hash(request_data.password)
        db.add(model_data)
        db.commit()
        db.refresh(model_data)

        detail_model = db.query(OrdinaryUserDetail).filter(
            OrdinaryUserDetail.user_id == model_data.id
        ).first()

        if not detail_model:
            detail_model = OrdinaryUserDetail(user_id=model_data.id)

        if request_data.photo:
            detail_model.photo = await handle_file_upload(
                request_data.photo, USER_DIR, detail_model.photo
            )

        detail_model.gender = request_data.gender
        detail_model.country_id = request_data.country_id
        detail_model.state_id = request_data.state_id
        detail_model.city_id = request_data.city_id
        detail_model.photo_approve = request_data.photo_approve

        db.add(detail_model)
        db.commit()

        return JSONResponse(
            content={
                "status": "success",
                "message": f"User {message} successfully",
                "user_id": model_data.id
            },
            status_code=200
        )

    except Exception as err:
        db.rollback()
        return JSONResponse(
            content={"status": "error", "message": str(err)},
            status_code=200
        )


async def handleGallerySave(request_data, db):

    try:
        if request_data.id is None:
            model_data = MediaGallery()
            message = "inserted"
        else:
            model_data = db.query(MediaGallery).filter(
                MediaGallery.id == request_data.id
            ).first()

            if not model_data:
                return JSONResponse(
                    content={"status": "error",
                             "message": "Record not found!"},
                    status_code=200
                )

            message = "updated"

        model_data.status = request_data.status
        if request_data.media_name:
            model_data.media_name = await handle_file_upload(
                request_data.media_name, PHOTO_DIR, model_data.media_name
            )
        db.add(model_data)
        db.commit()
        db.refresh(model_data)

        return JSONResponse(
            content={
                "status": "success",
                "message": f"Photo Gallery {message} successfully",
                "user_id": model_data.id
            },
            status_code=200
        )

    except Exception as err:
        db.rollback()
        return JSONResponse(
            content={"status": "error", "message": str(err)},
            status_code=200
        )


async def handleCmsPageSave(request_data, db):
    try:
        if request_data.id is None:
            if db.query(CmsPage).filter(CmsPage.page_title == request_data.page_title).first():
                return JSONResponse(
                    content={"status": "error",
                             "message": "page_title has already been taken"},
                    status_code=200
                )
            model_data = CmsPage()
            message = "Inserted"

        else:
            model_data = db.query(CmsPage).filter(
                CmsPage.id == request_data.id).first()
            if not model_data:
                return JSONResponse(
                    content={"status": "error",
                             "message": "Record Not Found For Update"},
                    status_code=200
                )

            if (
                model_data.page_title != request_data.page_title
                and db.query(CmsPage).filter(CmsPage.page_title == request_data.page_title).first()
            ):
                return JSONResponse(
                    content={"status": "error",
                             "message": "page_title has already been taken"},
                    status_code=200
                )
            message = "Updated"

        if request_data.meta_image:
            model_data.meta_image = await handle_file_upload(
                request_data.meta_image, CMS_IMG_DIR, model_data.meta_image
            )

        model_data.status = request_data.status
        model_data.page_title = request_data.page_title
        model_data.page_content = request_data.page_content
        model_data.meta_title = request_data.meta_title
        model_data.meta_description = request_data.meta_description
        model_data.display_footer = request_data.display_footer

        db.add(model_data)
        db.commit()

        return JSONResponse(
            content={"status": "success",
                     "message": f"Cms Page {message} successfully"},
            status_code=200
        )

    except Exception as err:
        db.rollback()
        return JSONResponse(
            content={"status": "error", "message": f"ad{str(err)}"},
            status_code=200
        )
