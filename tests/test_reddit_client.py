import pytest
from reddit_api.errors import RedditAuthenticationError, RedditTimeoutError
from unittest.mock import Mock
import requests


def test__get_token__return_token_on_success_response(reddit_client, requests_post_mock):
    mock_response = Mock()
    mock_response.json.return_value = {"access_token": "mock_token"}
    requests_post_mock.return_value = mock_response
    token = reddit_client.get_token()
    assert token == "mock_token"


def test__get_token__raise_error(reddit_client, requests_post_mock):
    requests_post_mock.side_effect = requests.exceptions.RequestException("Mock error")
    with pytest.raises(requests.exceptions.RequestException):
        reddit_client.get_token()


def test__make_authenticated_request__correctly_parses_response(
        reddit_client,
        requests_get_mock,
        mock_get_token):

    mock_get_token.return_value = "mock_token"
    mock_response = Mock()
    mock_response.json.return_value = {"data": {"after": "mock_value", "children": [1, 2]}}
    requests_get_mock.return_value = mock_response

    response = reddit_client.make_authenticated_request("mock_url")

    assert response.after == "mock_value"
    assert response.children == [1, 2]


def test__make_authenticated_request__raise_reddit_authentication_error(
        reddit_client,
        requests_post_mock):

    requests_post_mock.side_effect = RedditAuthenticationError
    with pytest.raises(RedditAuthenticationError):
        reddit_client.make_authenticated_request("mock_url")


def test__make_authenticated_request__raise_reddit_timeout_error(
        reddit_client,
        requests_post_mock):

    requests_post_mock.side_effect = RedditTimeoutError
    with pytest.raises(RedditTimeoutError):
        reddit_client.make_authenticated_request("mock_url")
