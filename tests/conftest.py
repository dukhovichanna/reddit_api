import pytest
from reddit_api.models import Response, Post, Comment
from reddit_api.reddit_client import RedditClient
from reddit_api.config import config
from typing import Dict, Optional


@pytest.fixture
def reddit_client():
    return RedditClient(
        client_id=config.client_id,
        client_secret=config.secret,
        username=config.username,
        password=config.password,
        user_agent=config.user_agent,
        api_url=config.api_url
    )

@pytest.fixture
def make_comment():
    def inner(
        author: str = 'John',
        permalink: str = '/r/books/comments/19cfrzw/user_comment',
        replies: Optional[Dict] = {"data": {"after": "a1s2d3f4", "children": [1, 2]}}
    ):
        return Comment(author=author, permalink=permalink, replies=replies)

    return inner

@pytest.fixture
def list_of_comments(make_comment):
    list_of_comments=[]
    for i in range(20):
        if i % 4:
            list_of_comments.append(make_comment(author='Jane', replies=''))
        elif i % 3:
            list_of_comments.append(make_comment(author='Jack'))
        elif i % 2:
            list_of_comments.append(make_comment(author='Jim'))
        else:
            list_of_comments.append(make_comment())
    return list_of_comments