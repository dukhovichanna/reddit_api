from typing import Optional
from pydantic import BaseModel, validator
from datetime import datetime


class Response(BaseModel):
    after: str | None
    children: list


class Post(BaseModel):
    author: str
    created: datetime
    permalink: str

    @property
    def comments_url(self) -> str:
        return f"https://oauth.reddit.com{self.permalink}.json"


class Comment(BaseModel):
    author: str
    permalink: str
    replies: Optional[dict]

    @validator("replies", pre=True, always=True)
    def convert_empty_string_to_none(cls: BaseModel, value: str) -> str | None:
        if value == '':
            return None
        return value
