from typing import Optional, Dict, List
from pydantic import BaseModel, validator
from datetime import datetime
from reddit_api.config import config


class Response(BaseModel):
    after: str | None
    children: List


class Post(BaseModel):
    author: str
    created: datetime
    permalink: str

    @property
    def comments_url(self) -> str:
        return f"{config.oauth_url}{self.permalink}.json"


class Comment(BaseModel):
    author: str
    permalink: str
    replies: Optional[Dict]

    @validator("replies", pre=True, always=True)
    def convert_empty_string_to_none(cls: BaseModel, value: str) -> str | None:
        if value == '':
            return None
        return value
