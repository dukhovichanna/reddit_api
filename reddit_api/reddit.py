from reddit_api.models import Response
from reddit_api.models import Post, Comment
from typing import Any
import requests
import logging

logger = logging.getLogger(__name__)


class RedditClient:

    def __init__(self, client_id, client_secret, username, password, user_agent, api_url):
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self.user_agent = user_agent
        self.api_url = api_url

    def get_token(self) -> str:
        logger.debug("Getting token...")
        headers = {"User-Agent": self.user_agent}
        data = {
            "grant_type": "password",
            "username": self.username,
            "password": self.password
        }
        auth = requests.auth.HTTPBasicAuth(self.client_id, self.client_secret)
        url = 'https://www.reddit.com/api/v1/access_token'

        try:
            response = requests.post(url=url, data=data, headers=headers, auth=auth)
            response.raise_for_status()
            return response.json()["access_token"]
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting token: {e}")
            raise

    @property
    def token(self) -> str:
        if self._token:
            return self._token
        
        # TODO: Check the validity of the tocken

        self._token = self.get_token()
        return self._token
    
    @property
    def headers(self) -> dict[str, str]:
        return {"User-Agent": self.user_agent, "Authorization": f"bearer {self.token}"}


    def get_posts(self, subreddit_name: str,
                  after: str | None = None, # TODO: add 'after', if none ...
                  limit: int = 100) -> list[Post]:

        url = f'https://oauth.reddit.com/r/{subreddit_name}/new'

        params = {'t': 'all', 'limit': limit}

        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            payload = response.json()
            reddit_response = Response(**payload['data'])
            return [Post(**item['data']) for item in reddit_response.children]

        except requests.exceptions.RequestException as e:
            logger.error(f"Error making authenticated request: {e}")
            raise


    def get_comments(self, post: Post) -> list[Comment]:

        try:
            response = requests.get(post.comments_url, headers=self.headers)
            response.raise_for_status()
            payload = response.json()
            
            comment_response = Response(**payload[1]['data'])
            comments = []

            self.extract_comments_from_response(comment_response.children, comments)

        except requests.exceptions.RequestException as e:
            logger.error(f"Error making authenticated request: {e}")
            raise


    def extract_comments_from_response(self,
        comment_data: list[dict[str, Any]],
        comments_list: list[Comment]) -> None:
        for comment_info in comment_data:
            if 'author' in comment_info['data']:
                comment = Comment(**comment_info['data'])
                comments_list.append(comment)
                if comment.replies:
                    self.extract_comments_from_response(comment.replies['data']['children'], comments_list)






