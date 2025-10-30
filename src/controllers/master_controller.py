from ..models import BannerModel as Banner, CategoryModel as Category, CurrencyModel as Currency
from fastapi.responses import JSONResponse
import os
import time
import uuid


UPLOAD_DIR = "uploads"
BANNER_DIR = os.path.join(UPLOAD_DIR, "banner")
CATEGORY_DIR = os.path.join(UPLOAD_DIR, "category")


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


def handle_not_found(model_data):
    """Return a JSON error if the record is not found."""
    if not model_data:
        return JSONResponse(
            content={"status": "error", "message": "Record not found!"},
            status_code=200
        )
    return None


async def handleBannerSave(request_data, db):

    try:
        if request_data.id is None:

            if db.query(Banner).filter(
                Banner.banner_title == request_data.banner_title
            ).first():
                return JSONResponse(
                    content={"status": "error",
                             "message": "banner_title has already been taken."},
                    status_code=200
                )
            model_data = Banner()
            message = "inserted"
        else:
            model_data = db.query(Banner).filter(
                Banner.id == request_data.id
            ).first()

            if (err := handle_not_found(model_data)):
                return err

            if db.query(Banner).filter(
                Banner.banner_title == request_data.banner_title, Banner.id != request_data.id
            ).first():
                return JSONResponse(
                    content={"status": "error",
                             "message": "banner_title has already been taken."},
                    status_code=200
                )

            message = "updated"

        if request_data.banner:
            model_data.banner = await handle_file_upload(
                request_data.banner, BANNER_DIR, model_data.banner
            )

        model_data.banner_title = request_data.banner_title
        model_data.button_text = request_data.button_text
        model_data.link = request_data.link
        model_data.status = request_data.status

        db.add(model_data)
        db.commit()
        db.refresh(model_data)

        return JSONResponse(
            content={
                "status": "success",
                "message": f"Banner {message} successfully",
            },
            status_code=200
        )

    except Exception as err:
        db.rollback()
        return JSONResponse(
            content={"status": "error", "message": str(err)},
            status_code=200
        )


async def handleCategorySave(request_data, db):

    try:
        if request_data.id is None:
            if db.query(Category).filter(
                Category.category_name == request_data.category_name
            ).first():
                return JSONResponse(
                    content={"status": "error",
                             "message": "category_name has already been taken."},
                    status_code=200
                )
            model_data = Category()
            message = "inserted"
        else:
            model_data = db.query(Category).filter(
                Category.id == request_data.id
            ).first()

            if (err := handle_not_found(model_data)):
                return err

            if db.query(Category).filter(
                Category.category_name == request_data.category_name, Category.id != request_data.id
            ).first():
                return JSONResponse(
                    content={"status": "error",
                             "message": "category_name has already been taken."},
                    status_code=200
                )

            message = "updated"

        if request_data.category_icon:
            model_data.category_icon = await handle_file_upload(
                request_data.category_icon, BANNER_DIR, model_data.category_icon
            )

        model_data.category_name = request_data.category_name
        model_data.seo_title = request_data.seo_title
        model_data.seo_keyword = request_data.seo_keyword
        model_data.display_home_page = request_data.display_home_page
        model_data.seo_description = request_data.seo_description
        model_data.status = request_data.status

        db.add(model_data)
        db.commit()
        db.refresh(model_data)

        return JSONResponse(
            content={
                "status": "success",
                "message": f"Category {message} successfully",
            },
            status_code=200
        )

    except Exception as err:
        db.rollback()
        return JSONResponse(
            content={"status": "error", "message": str(err)},
            status_code=200
        )


async def handleCurrencySave(request_data, db):

    try:
        if request_data.id is None:
            if db.query(Currency).filter(
                Currency.currency_name == request_data.currency_name
            ).first():
                return JSONResponse(
                    content={"status": "error",
                             "message": "currency_name has already been taken."},
                    status_code=200
                )
            model_data = Currency()
            message = "inserted"
        else:
            model_data = db.query(Currency).filter(
                Currency.id == request_data.id
            ).first()

            if (err := handle_not_found(model_data)):
                return err

            if db.query(Currency).filter(
                Currency.currency_name == request_data.currency_name, Currency.id != request_data.id
            ).first():
                return JSONResponse(
                    content={"status": "error",
                             "message": "currency_name has already been taken."},
                    status_code=200
                )

            message = "updated"

        model_data.currency_name = request_data.currency_name
        model_data.currency_code = request_data.currency_code
        model_data.symbol = request_data.symbol
        model_data.status = request_data.status

        db.add(model_data)
        db.commit()
        db.refresh(model_data)

        return JSONResponse(
            content={
                "status": "success",
                "message": f"Currency {message} successfully",
            },
            status_code=200
        )

    except Exception as err:
        db.rollback()
        return JSONResponse(
            content={"status": "error", "message": str(err)},
            status_code=200
        )
