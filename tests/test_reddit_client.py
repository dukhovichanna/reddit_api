import pytest
from unittest.mock import patch, Mock
from reddit_api.models import Response
import requests


def test__get_token__success(reddit_client):
    with patch('requests.post') as mock_post:
        mock_response = Mock()
        mock_response.json.return_value = {"access_token": "mock_token"}
        mock_post.return_value = mock_response
        token = reddit_client.get_token()
        assert token == "mock_token"


def test__get_token__failure(reddit_client):
    with patch('requests.post') as mock_post:
        mock_post.side_effect = requests.exceptions.RequestException("Mock error")
        with pytest.raises(requests.exceptions.RequestException):
            reddit_client.get_token()


def test__make_authenticated_request__correctly_parses_response(reddit_client):
    with patch('reddit_api.reddit_client.requests.get') as mock_get, \
            patch('reddit_api.reddit_client.RedditClient.get_token') as mock_get_token:
        mock_get_token.return_value = "mock_token"
        mock_response = Mock()
        mock_response.json.return_value = {"data": {"after": "mock_value", "children": [1, 2]}}
        mock_get.return_value = mock_response
        response = reddit_client.make_authenticated_request("mock_url")
        assert response.after == "mock_value"
        assert response.children == [1, 2]


def test__make_authenticated_request__failure(reddit_client):
    with patch('requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.RequestException("Mock error")
        with pytest.raises(requests.exceptions.RequestException):
            reddit_client.make_authenticated_request("mock_url")
