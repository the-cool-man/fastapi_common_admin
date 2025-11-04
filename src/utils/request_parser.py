from fastapi import Request, UploadFile
from starlette.datastructures import UploadFile as StarletteUploadFile
from typing import Type, TypeVar
from pydantic import ValidationError
from sqlalchemy.ext.declarative import declared_attr
from datetime import datetime, date
from decimal import Decimal
from sqlalchemy.ext.declarative import as_declarative, declared_attr


T = TypeVar("T")


class MultiFormatRequest:
    @classmethod
    async def from_request(cls: Type[T], request: Request) -> T:
        content_type = request.headers.get("content-type", "")
        data = {}

        if not content_type:
            return cls(**data)

        if "application/json" in content_type:
            data = await request.json()

        elif "application/x-www-form-urlencoded" in content_type or "multipart/form-data" in content_type:
            form = await request.form()
            data = {}

            for key, value in form.multi_items():
                clean_key = key.replace("[]", "")
                if isinstance(value, (UploadFile, StarletteUploadFile)):
                    data[clean_key] = value
                    continue

                if key.endswith("[]") or clean_key == "checkbox_val":
                    if clean_key in data:
                        data[clean_key].append(value)
                    else:
                        data[clean_key] = [value]
                else:
                    if clean_key in data:
                        if isinstance(data[clean_key], list):
                            data[clean_key].append(value)
                        else:
                            data[clean_key] = [data[clean_key], value]
                    else:
                        data[clean_key] = value

        else:
            raise ValueError(f"Unsupported content type: {content_type}")

        return cls(**data)


@as_declarative()
class BaseDic:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def as_dict(self, exclude_fields=None, base_url=None):
        if exclude_fields is None:
            exclude_fields = []

        result = {}
        for c in self.__table__.columns:
            if c.name in exclude_fields:
                continue

            value = getattr(self, c.name)
            if isinstance(value, (datetime, date)):
                result[c.name] = value.isoformat()
            elif isinstance(value, Decimal):
                result[c.name] = float(value)
            else:
                result[c.name] = value

        if base_url:
            possible_image_fields = [
                "social_logo", "meta_image", "banner", "category_icon", "photo"]
            for field in possible_image_fields:
                if hasattr(self, field):
                    image_value = getattr(self, field)
                    if image_value:
                        result["image_full_url"] = f"{base_url}/{image_value}"
                        break
            else:
                result["image_full_url"] = None
        return result
