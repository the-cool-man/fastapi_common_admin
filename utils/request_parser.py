from fastapi import Request, UploadFile
from starlette.datastructures import UploadFile as StarletteUploadFile
from typing import Type, TypeVar
from pydantic import ValidationError


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
