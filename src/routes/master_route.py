from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse
from typing import Annotated
from ..schemas import ListDataSchema, BannerSchema, CategorySchema, CurrencySchema, GstPercentageSchema, CountrySchema, StateSchema, CitySchema
from ..utils import check_token_response, status_update, sort_search_paginate_data, validate_token, edit_data
from ..db_connection import DBSession
from ..models import BannerModel as Banner, CategoryModel as Category, CurrencyModel as Currency, GstPercentageModel as GST, CountryModel as Country, StateModel as State, CityModel as City
from ..controllers import handleBannerSave, handleCategorySave, handleCurrencySave, handleGSTPercentageSave, handleCountrySave, handleStateSave, handleCitySave

router = APIRouter()


# BANNER ROUTE ----------------------------

@router.post("/banner-list")
def banner_get_data(request_data: Annotated[ListDataSchema, Depends(ListDataSchema.from_request)], db: DBSession, page: int = Query(1, g=1), valid_token=Depends(validate_token)):

    if (res := check_token_response(valid_token)):
        return res

    # STATUS UPDATE -------------------------

    if request_data.status_update in ["A", "I", "DELETE"] and len(request_data.checkbox_val) > 0:
        return status_update(request_data, db, Banner)

    # SORTING, SEARCHING AND PAGINATION -------------------------

    query = db.query(Banner)
    response_data = sort_search_paginate_data(
        request_data, db, Banner, query, page, search_column="banner_title", folder="banner")

    return JSONResponse(content=response_data, status_code=200)


@router.post("/banner-save")
async def banner_save_data(
    request_data: Annotated[BannerSchema, Depends(BannerSchema.from_request)],
    db: DBSession,
    valid_token=Depends(validate_token)
):
    if (res := check_token_response(valid_token)):
        return res

    return await handleBannerSave(request_data, db)


@router.get("/banner-list/edit/{edit_id}")
def banner_edit_data(edit_id: int, db: DBSession, valid_token=Depends(validate_token)):

    if (res := check_token_response(valid_token)):
        return res

    return edit_data(db, Banner, edit_id, folder="banner")


# CATEGORY ROUTE ----------------------------

@router.post("/category-list")
def category_get_data(request_data: Annotated[ListDataSchema, Depends(ListDataSchema.from_request)], db: DBSession, page: int = Query(1, g=1), valid_token=Depends(validate_token)):

    if (res := check_token_response(valid_token)):
        return res

    # STATUS UPDATE -------------------------

    if request_data.status_update in ["A", "I", "DELETE"] and len(request_data.checkbox_val) > 0:
        return status_update(request_data, db, Category)

    # SORTING, SEARCHING AND PAGINATION -------------------------

    query = db.query(Category)
    response_data = sort_search_paginate_data(
        request_data, db, Category, query, page, search_column="category_name", folder="category")

    return JSONResponse(content=response_data, status_code=200)


@router.post("/category-save")
async def category_save_data(
    request_data: Annotated[CategorySchema, Depends(CategorySchema.from_request)],
    db: DBSession,
    valid_token=Depends(validate_token)
):
    if (res := check_token_response(valid_token)):
        return res

    return await handleCategorySave(request_data, db)


@router.get("/category-list/edit/{edit_id}")
def category_edit_data(edit_id: int, db: DBSession, valid_token=Depends(validate_token)):

    if (res := check_token_response(valid_token)):
        return res

    return edit_data(db, Category, edit_id, folder="category")


# CURRENCY ROUTE ----------------------------

@router.post("/currency-list")
def category_get_data(request_data: Annotated[ListDataSchema, Depends(ListDataSchema.from_request)], db: DBSession, page: int = Query(1, g=1), valid_token=Depends(validate_token)):

    if (res := check_token_response(valid_token)):
        return res

    # STATUS UPDATE -------------------------

    if request_data.status_update in ["A", "I", "DELETE"] and len(request_data.checkbox_val) > 0:
        return status_update(request_data, db, Currency)

    # SORTING, SEARCHING AND PAGINATION -------------------------

    query = db.query(Currency)
    response_data = sort_search_paginate_data(
        request_data, db, Currency, query, page, search_column="currency_name")

    return JSONResponse(content=response_data, status_code=200)


@router.post("/currency-save")
async def category_save_data(
    request_data: Annotated[CurrencySchema, Depends(CurrencySchema.from_request)],
    db: DBSession,
    valid_token=Depends(validate_token)
):
    if (res := check_token_response(valid_token)):
        return res

    return await handleCurrencySave(request_data, db)


@router.get("/currency-list/edit/{edit_id}")
def category_edit_data(edit_id: int, db: DBSession, valid_token=Depends(validate_token)):

    if (res := check_token_response(valid_token)):
        return res

    return edit_data(db, Currency, edit_id)


# GST PERCENTAGE ROUTE ----------------------------

@router.post("/gst-percentage-list")
def gst_get_data(request_data: Annotated[ListDataSchema, Depends(ListDataSchema.from_request)], db: DBSession, page: int = Query(1, g=1), valid_token=Depends(validate_token)):

    if (res := check_token_response(valid_token)):
        return res

    # STATUS UPDATE -------------------------

    if request_data.status_update in ["A", "I", "DELETE"] and len(request_data.checkbox_val) > 0:
        return status_update(request_data, db, GST)

    # SORTING, SEARCHING AND PAGINATION -------------------------

    query = db.query(GST)
    response_data = sort_search_paginate_data(
        request_data, db, GST, query, page, search_column="gst_percentage")

    return JSONResponse(content=response_data, status_code=200)


@router.post("/gst-percentage-save")
async def gst_save_data(
    request_data: Annotated[GstPercentageSchema, Depends(GstPercentageSchema.from_request)],
    db: DBSession,
    valid_token=Depends(validate_token)
):
    if (res := check_token_response(valid_token)):
        return res

    return await handleGSTPercentageSave(request_data, db)


@router.get("/gst-percentage-list/edit/{edit_id}")
def gst_edit_data(edit_id: int, db: DBSession, valid_token=Depends(validate_token)):

    if (res := check_token_response(valid_token)):
        return res

    return edit_data(db, GST, edit_id)


# COUNTRY ROUTE ----------------------------

@router.post("/country-list")
def country_get_data(request_data: Annotated[ListDataSchema, Depends(ListDataSchema.from_request)], db: DBSession, page: int = Query(1, g=1), valid_token=Depends(validate_token)):

    if (res := check_token_response(valid_token)):
        return res

    # STATUS UPDATE -------------------------

    if request_data.status_update in ["A", "I", "DELETE"] and len(request_data.checkbox_val) > 0:
        return status_update(request_data, db, Country)

    # SORTING, SEARCHING AND PAGINATION -------------------------

    query = db.query(Country)
    response_data = sort_search_paginate_data(
        request_data, db, Country, query, page, search_column="country_name")

    return JSONResponse(content=response_data, status_code=200)


@router.post("/country-save")
async def country_save_data(
    request_data: Annotated[CountrySchema, Depends(CountrySchema.from_request)],
    db: DBSession,
    valid_token=Depends(validate_token)
):
    if (res := check_token_response(valid_token)):
        return res

    return await handleCountrySave(request_data, db)


@router.get("/country-list/edit/{edit_id}")
def country_edit_data(edit_id: int, db: DBSession, valid_token=Depends(validate_token)):

    if (res := check_token_response(valid_token)):
        return res

    return edit_data(db, Country, edit_id)


# STATE ROUTE ----------------------------

@router.post("/state-list")
def state_get_data(request_data: Annotated[ListDataSchema, Depends(ListDataSchema.from_request)], db: DBSession, page: int = Query(1, g=1), valid_token=Depends(validate_token)):

    if (res := check_token_response(valid_token)):
        return res

    # STATUS UPDATE -------------------------

    if request_data.status_update in ["A", "I", "DELETE"] and len(request_data.checkbox_val) > 0:
        return status_update(request_data, db, State)

    # SORTING, SEARCHING AND PAGINATION -------------------------

    query = db.query(State)
    response_data = sort_search_paginate_data(
        request_data, db, State, query, page, search_column="state_name")

    return JSONResponse(content=response_data, status_code=200)


@router.post("/state-save")
async def state_save_data(
    request_data: Annotated[StateSchema, Depends(StateSchema.from_request)],
    db: DBSession,
    valid_token=Depends(validate_token)
):
    if (res := check_token_response(valid_token)):
        return res

    return await handleStateSave(request_data, db)


@router.get("/state-list/edit/{edit_id}")
def state_edit_data(edit_id: int, db: DBSession, valid_token=Depends(validate_token)):

    if (res := check_token_response(valid_token)):
        return res

    return edit_data(db, State, edit_id)


# @router.post("/statelist/{edit_id}")
# def state_edit_data(edit_id: int, db: DBSession, valid_token=Depends(validate_token)):

#     if (res := check_token_response(valid_token)):
#         return res

#     return edit_data(db, Country, edit_id)


# CITY ROUTE ----------------------------

@router.post("/city-list-data")
def city_get_data(request_data: Annotated[ListDataSchema, Depends(ListDataSchema.from_request)], db: DBSession, page: int = Query(1, g=1), valid_token=Depends(validate_token)):

    if (res := check_token_response(valid_token)):
        return res

    # STATUS UPDATE -------------------------

    if request_data.status_update in ["A", "I", "DELETE"] and len(request_data.checkbox_val) > 0:
        return status_update(request_data, db, City)

    # SORTING, SEARCHING AND PAGINATION -------------------------

    query = db.query(City)
    response_data = sort_search_paginate_data(
        request_data, db, City, query, page, search_column="city_name")

    return JSONResponse(content=response_data, status_code=200)


@router.post("/city-save")
async def city_save_data(
    request_data: Annotated[CitySchema, Depends(CitySchema.from_request)],
    db: DBSession,
    valid_token=Depends(validate_token)
):
    if (res := check_token_response(valid_token)):
        return res

    return await handleCitySave(request_data, db)


@router.get("/city-list-data/edit/{edit_id}")
def city_edit_data(edit_id: int, db: DBSession, valid_token=Depends(validate_token)):

    if (res := check_token_response(valid_token)):
        return res

    return edit_data(db, City, edit_id)
