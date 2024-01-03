from dataclasses import dataclass
from typing import Any, Dict
import requests
import logging

REDDIT_API_URL = 'https://www.reddit.com/api/v1/access_token'

logger = logging.getLogger(__name__)


@dataclass
class RedditClient:
    client_id: str
    client_secret: str
    username: str
    password: str
    user_agent: str

    def get_token(self) -> str:
        logger.debug("Getting token...")
        headers = {"User-Agent": self.user_agent}
        data = {
            "grant_type": "password",
            "username": self.username,
            "password": self.password
        }
        auth = requests.auth.HTTPBasicAuth(self.client_id, self.client_secret)
        response = requests.post(REDDIT_API_URL, data=data, headers=headers, auth=auth)
        return response.json()["access_token"]

    def make_authenticated_request(self, url: str, params: Dict[str, Any] | None = None) -> Dict:
        headers = {"User-Agent": self.user_agent, "Authorization": f"bearer {self.get_token()}"}
        response = requests.get(url, headers=headers, params=params)
        return response.json()
