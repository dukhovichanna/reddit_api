import pytest
from reddit_api.models import Response, Comment
from reddit_api.reddit_client import RedditClient
from unittest.mock import patch
from typing import Any


@pytest.fixture
def reddit_client(faker):
    return RedditClient(
        client_id=faker.pystr(),
        client_secret=faker.pystr(),
        username=faker.pystr(),
        password=faker.pystr(),
        user_agent=faker.pystr()
    )


@pytest.fixture
def make_comment():
    def inner(
        author: str | None = None,
        permalink: str | None = None,
        replies: dict[str, Any] | None = None
    ):
        return Comment(
            author=author or 'John',
            permalink=permalink or '/r/books/comments/19cfrzw/user_comment',
            replies=replies or {"data": {"after": "a1s2d3f4", "children": [1, 2]}})

    return inner

@pytest.fixture
def make_many_comments(make_comment):
    def inner(
        users: dict[str, int] | None = None, 
        unique: int = 0,
    ):
        comments = []
        for user, comments_count in users.items():
            for _ in range(comments_count):
                comment = make_comment(author=user, replies='')
                comments.append(comment)

        for _ in range(unique):
            comment = make_comment()
            comments.append(comment)

        return comments
    return inner

@pytest.fixture
def list_of_comments_with_preset_data(make_many_comments):
    return make_many_comments(
        users={'Jane': 15, 'Jack': 3, 'John': 2}
    )


@pytest.fixture
def make_post_response():
    def inner(
        after: str = 't3_19a64l6',
        author: str = 'throwawayhelp62525',
        permalink: str = '/r/books/comments/19cfrzw/my_comment/',
        created: float = 1705876122.0
    ):
        return Response(
            after=after,
            children=[{
                "data": {
                    "created": created,
                    "author": author,
                    "permalink": permalink
                }
            }]
        )
    return inner


@pytest.fixture
def regular_post_response(make_post_response):
    return make_post_response()


@pytest.fixture
def response_with_post_outside_timelimit(make_post_response):
    return make_post_response(created=1643200000)


@pytest.fixture
def comment_data():
    return [
        {'data': {'author': 'user1', 'replies': None, 'permalink': '/r/books/comments/1/'}},
        {'data': {'author': 'user2', 'replies': None, 'permalink': '/r/books/comments/2/'}}
    ]


@pytest.fixture
def comment_data_with_nested_replies(comment_data):
    return [
        {
            'data': {
                'author': 'user1',
                'permalink': '/r/books/comments/19cfrzw/my_comment/',
                'replies': {
                    'data': {
                        'children': comment_data
                    }
                }
            }
        }
    ]


@pytest.fixture
def requests_get_mock():
    with patch('requests.get') as mock:
        yield mock


@pytest.fixture
def requests_post_mock():
    with patch('requests.post') as mock:
        yield mock
