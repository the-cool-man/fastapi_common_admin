from pydantic import BaseModel
from ..utils import MultiFormatRequest
from typing import Optional


class ListDataSchema(BaseModel, MultiFormatRequest):
    sort_order: Optional[str] = "DESC"
    sort_column: Optional[str] = "id"
    search_field: Optional[str] = None
    limit_per_page: Optional[int] = 10
    page: Optional[int] = 1
    status_update: Optional[str] = "A"
    checkbox_val: Optional[list] = []
