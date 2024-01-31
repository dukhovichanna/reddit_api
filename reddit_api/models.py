from typing import Optional
from pydantic import BaseModel, field_validator
from datetime import datetime


class Response(BaseModel):
    after: str | None
    children: list


class Post(BaseModel):
    author: str
    created: datetime
    permalink: str


class Comment(BaseModel):
    author: str
    permalink: str
    replies: Optional[dict]

    @field_validator("replies", mode="before")
    def convert_empty_string_to_none(cls: BaseModel, value: str) -> str | None:
        if value == '':
            return None
        return value
