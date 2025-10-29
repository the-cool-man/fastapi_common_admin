from fastapi.responses import JSONResponse
from sqlalchemy import desc, asc


def check_token_response(valid_token):
    if isinstance(valid_token, JSONResponse):
        return valid_token
    return None


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


def sort_search_paginate_data(request_data, db, Model, query, page):
    limit = getattr(request_data, "limit_per_page", 10) or 10
    sort_order = getattr(request_data, "sort_order", "ASC").upper()
    sort_column_name = getattr(request_data, "sort_column", "id")
    search_field_value = getattr(request_data, "search_field", None)
    print("search_field_value,search_column_name",
          search_field_value, sort_column_name)
    if search_field_value and sort_column_name:
        search_column = getattr(Model, sort_column_name, None)
        if search_column is not None:
            search_value = f"%{search_field_value}%"
            query = query.filter(search_column.ilike(search_value))

    sort_column = getattr(Model, sort_column_name, None)
    if sort_column is not None:
        query = query.order_by(
            asc(sort_column) if sort_order == "ASC" else desc(sort_column))

    approve_count = db.query(Model).filter(Model.status == "A").count()
    unapprove_count = db.query(Model).filter(Model.status == "I").count()

    offset = (page - 1) * limit
    all_data = query.offset(offset).limit(limit).all()

    all_data_list = [row.as_dict() for row in all_data] if all_data else []

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


def edit_data(db, Model, edit_id):
    return db.query(Model).filter(Model.id == edit_id).first()
