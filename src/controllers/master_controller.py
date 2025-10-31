from ..models import BannerModel as Banner, CategoryModel as Category, CurrencyModel as Currency, GstPercentageModel as GST, CountryModel as Country, StateModel as State, CityModel as City
from fastapi.responses import JSONResponse
import os
import time
import uuid
import json
from pathlib import Path


UPLOAD_DIR = "uploads"
BANNER_DIR = os.path.join(UPLOAD_DIR, "banner")
CATEGORY_DIR = os.path.join(UPLOAD_DIR, "category")

iso_path = Path(__file__).parent.parent / "utils" / "country_to_iso.json"

with open(iso_path, "r", encoding="utf-8") as f:
    COUNTRY_TO_ISO = json.load(f)


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
                request_data.category_icon, CATEGORY_DIR, model_data.category_icon
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


async def handleGSTPercentageSave(request_data, db):

    try:
        if request_data.id is None:
            if db.query(GST).filter(
                GST.gst_percentage == request_data.gst_percentage
            ).first():
                return JSONResponse(
                    content={"status": "error",
                             "message": "gst_percentage has already been taken."},
                    status_code=200
                )
            model_data = GST()
            message = "inserted"
        else:
            model_data = db.query(GST).filter(
                GST.id == request_data.id
            ).first()

            if (err := handle_not_found(model_data)):
                return err

            if db.query(GST).filter(
                GST.gst_percentage == request_data.gst_percentage, Currency.id != request_data.id
            ).first():
                return JSONResponse(
                    content={"status": "error",
                             "message": "gst_percentage has already been taken."},
                    status_code=200
                )

            message = "updated"

        model_data.gst_percentage = request_data.gst_percentage
        model_data.status = request_data.status

        db.add(model_data)
        db.commit()
        db.refresh(model_data)

        return JSONResponse(
            content={
                "status": "success",
                "message": f"GST Percentage {message} successfully",
            },
            status_code=200
        )

    except Exception as err:
        db.rollback()
        return JSONResponse(
            content={"status": "error", "message": str(err)},
            status_code=200
        )


async def handleCountrySave(request_data, db):
    try:
        if request_data.id is None:
            # Insert
            if db.query(Country).filter(
                Country.country_name == request_data.country_name
            ).first():
                return JSONResponse(
                    content={"status": "error",
                             "message": "country_name has already been taken."},
                    status_code=200
                )
            model_data = Country()
            message = "inserted"
        else:
            # Update
            model_data = db.query(Country).filter(
                Country.id == request_data.id
            ).first()

            if (err := handle_not_found(model_data)):
                return err

            if db.query(Country).filter(
                Country.country_name == request_data.country_name,
                Country.id != request_data.id
            ).first():
                return JSONResponse(
                    content={"status": "error",
                             "message": "country_name has already been taken."},
                    status_code=200
                )
            message = "updated"

        # Set fields
        iso_code = COUNTRY_TO_ISO.get(request_data.country_name, None)
        model_data.country_name = request_data.country_name
        model_data.country_code = f"+{request_data.country_code}"
        model_data.flag = iso_code
        model_data.status = request_data.status

        db.add(model_data)
        db.commit()
        db.refresh(model_data)

        return JSONResponse(
            content={
                "status": "success",
                "message": f"country {message} successfully",
            },
            status_code=200
        )

    except Exception as err:
        db.rollback()
        return JSONResponse(
            content={"status": "error", "message": str(err)},
            status_code=200
        )


async def handleStateSave(request_data, db):
    try:
        if request_data.id is None:
            # Insert
            if db.query(State).filter(
                State.state_name == request_data.state_name
            ).first():
                return JSONResponse(
                    content={"status": "error",
                             "message": "state_name has already been taken."},
                    status_code=200
                )
            model_data = State()
            message = "inserted"
        else:
            # Update
            model_data = db.query(State).filter(
                State.id == request_data.id
            ).first()

            if (err := handle_not_found(model_data)):
                return err

            if db.query(State).filter(
                State.state_name == request_data.state_name,
                State.id != request_data.id
            ).first():
                return JSONResponse(
                    content={"status": "error",
                             "message": "state_name has already been taken."},
                    status_code=200
                )
            message = "updated"

        # Set fields
        model_data.state_name = request_data.state_name
        model_data.country_id = request_data.country_id
        model_data.status = request_data.status

        db.add(model_data)
        db.commit()
        db.refresh(model_data)

        return JSONResponse(
            content={
                "status": "success",
                "message": f"state {message} successfully",
            },
            status_code=200
        )

    except Exception as err:
        db.rollback()
        return JSONResponse(
            content={"status": "error", "message": str(err)},
            status_code=200
        )


async def handleCitySave(request_data, db):
    try:
        if request_data.id is None:
            # Insert
            if db.query(City).filter(
                City.city_name == request_data.city_name
            ).first():
                return JSONResponse(
                    content={"status": "error",
                             "message": "city_name has already been taken."},
                    status_code=200
                )
            model_data = City()
            message = "inserted"
        else:
            # Update
            model_data = db.query(City).filter(
                City.id == request_data.id
            ).first()

            if (err := handle_not_found(model_data)):
                return err

            if db.query(City).filter(
                City.city_name == request_data.city_name,
                City.id != request_data.id
            ).first():
                return JSONResponse(
                    content={"status": "error",
                             "message": "city_name has already been taken."},
                    status_code=200
                )
            message = "updated"

        # Set fields
        model_data.city_name = request_data.city_name
        model_data.country_id = request_data.country_id
        model_data.state_id = request_data.state_id
        model_data.status = request_data.status

        db.add(model_data)
        db.commit()
        db.refresh(model_data)

        return JSONResponse(
            content={
                "status": "success",
                "message": f"city {message} successfully",
            },
            status_code=200
        )

    except Exception as err:
        db.rollback()
        return JSONResponse(
            content={"status": "error", "message": str(err)},
            status_code=200
        )
