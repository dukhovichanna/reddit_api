from dataclasses import dataclass
from reddit_api.models import Response
from reddit_api.errors import RedditAuthenticationError, RedditTimeoutError
from typing import Any
import requests
import logging

logger = logging.getLogger(__name__)


@dataclass
class RedditClient:
    client_id: str
    client_secret: str
    username: str
    password: str
    user_agent: str
    api_url: str

    def get_token(self) -> str:
        logger.debug("Getting token...")
        headers = {"User-Agent": self.user_agent}
        data = {
            "grant_type": "password",
            "username": self.username,
            "password": self.password
        }
        auth = requests.auth.HTTPBasicAuth(self.client_id, self.client_secret)

        try:
            response = requests.post(url=self.api_url, data=data, headers=headers, auth=auth)
            response.raise_for_status()
            return response.json()["access_token"]
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting token: {e}")
            raise

    def make_authenticated_request(
            self, url: str,
            params: dict[str, Any] | None = None) -> Response:

        headers = {"User-Agent": self.user_agent, "Authorization": f"bearer {self.get_token()}"}

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            if isinstance(response.json(), list):
                return Response(**response.json()[1]['data'])
            else:
                return Response(**response.json()['data'])
        except requests.exceptions.HTTPError as http_err:
            if http_err.response.status_code == 401:
                raise RedditAuthenticationError() from http_err
            elif http_err.response.status_code == 504:
                raise RedditTimeoutError() from http_err
            else:
                raise
