from fastapi.responses import JSONResponse
from sqlalchemy import desc, asc
from ..utils import get_request


def check_token_response(valid_token):
    if isinstance(valid_token, JSONResponse):
        return valid_token
    return None


def get_base_url(folder: str) -> str:
    request = get_request()
    base = str(request.base_url).rstrip("/")
    return f"{base}/api/uploads/{folder}"


def status_update(request_data, db, Model):
    try:
        query = db.query(Model).filter(
            Model.id.in_(request_data.checkbox_val))

        if request_data.status_update == "DELETE":
            rows_deleted = query.delete(synchronize_session=False)
            db.commit()

            if rows_deleted == 0:
                return JSONResponse(
                    content={"status": "error",
                             "message": "Record Not Found!"},
                    status_code=200
                )
            return JSONResponse(
                content={"status": "success",
                         "message": "Data deleted successfully!"},
                status_code=200
            )

        rows_updated = query.update(
            {Model.status: request_data.status_update},
            synchronize_session=False
        )
        db.commit()
        if rows_updated == 0:
            return JSONResponse(
                content={"status": "error",
                         "message": "Data Not Found!"},
                status_code=200
            )

        return JSONResponse(
            content={"status": "success",
                     "message": "Status updated successfully!"},
            status_code=200
        )

    except Exception as err:
        db.rollback()
        return JSONResponse(
            content={"status": "error", "message": str(err)},
            status_code=200
        )


def sort_search_paginate_data(request_data, db, Model, query, page, search_column, folder=None):
    limit = getattr(request_data, "limit_per_page", 10) or 10
    sort_order = getattr(request_data, "sort_order", "ASC").upper()
    sort_column_name = getattr(request_data, "sort_column", "id")
    search_field_value = getattr(request_data, "search_field", None)

    base_url = None
    if folder:
        base_url = get_base_url(folder)

    sort_column = getattr(Model, sort_column_name, None)
    if sort_column is not None:
        query = query.order_by(
            asc(sort_column) if sort_order == "ASC" else desc(sort_column))

    approve_count = db.query(Model).filter(Model.status == "A").count()
    unapprove_count = db.query(Model).filter(Model.status == "I").count()

    offset = (page - 1) * limit
    paged_data = query.offset(offset).limit(limit).all()

    all_data = paged_data
    if search_field_value and search_column:
        search_value = search_field_value.lower()
        filtered_data = []
        for row in paged_data:
            value = getattr(row, search_column, "")
            if value and search_value in str(value).lower():
                filtered_data.append(row)
        all_data = filtered_data

    all_data_list = [row.as_dict(base_url=base_url)
                     for row in all_data] if all_data else []

    response_data = {
        "status": "success",
        "message": "All Data Display",
        "data": {"data": all_data_list},
        "approve_count": approve_count,
        "unapprove_count": unapprove_count
    }

    if all_data_list:
        response_data["data"].update({
            "total": approve_count + unapprove_count,
            "current_page": page,
            "per_page": limit
        })

    return response_data


def edit_data(db, Model, edit_id, folder=None):
    edit_data = db.query(Model).filter(Model.id == edit_id).first()

    base_url = None
    if folder:
        base_url = get_base_url(folder)

    if edit_data is None:
        return JSONResponse(
            content={"status": "error", "message": "Record not found!"},
            status_code=200
        )

    return JSONResponse(
        content={"status": "success", "message": "Data Display!",
                 "data": edit_data.as_dict(base_url=base_url)},
        status_code=200
    )
