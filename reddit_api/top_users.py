from reddit_api.config import config
from datetime import datetime, timedelta
from collections import Counter
from typing import Dict, Any
import requests
import re
import logging

REDDIT_API_URL = 'https://www.reddit.com/api/v1/access_token'
REDDIT_OAUTH_URL = 'https://oauth.reddit.com'

logger = logging.getLogger(__name__)

def get_token(client_id: str, client_secret: str, username: str, password: str) -> str:
    logger.debug("Getting token...")
    headers = {"User-Agent": config.user_agent}
    data = {
        "grant_type": "password",
        "username": username,
        "password": password
    }
    auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    response = requests.post(REDDIT_API_URL, data=data, headers=headers, auth=auth)
    return response.json()["access_token"]

def make_authenticated_request(url: str, token: str, params=None): # TODO: Add annotation for output
    headers = {"User-Agent": config.user_agent, "Authorization": f"bearer {token}"}
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def convert_unix_timestamp(unix_timestamp: float) -> datetime:
    return datetime.utcfromtimestamp(unix_timestamp)

def get_date_limit(limit_in_days: int) -> datetime:
    if limit_in_days < 0:
        raise ValueError("The limit_in_days argument must be a non-negative integer.")
    return datetime.today() - timedelta(days=limit_in_days)

def create_subreddit_url(subreddit_name: str) -> str:
    if not re.match("^[a-zA-Z0-9_]+$", subreddit_name):
        raise ValueError("Subreddit name must only contain alphanumeric characters and underscores.")
    return f'https://oauth.reddit.com/r/{subreddit_name}/new'

def process_comments(comment_data: Dict[str, Any], comment_counter: Counter) -> None:
    if 'data' in comment_data and 'children' in comment_data['data']:
        for comment in comment_data['data']['children']:
            if 'data' in comment and 'author' in comment['data']:
                comment_author = comment['data']['author']
                comment_counter[comment_author] += 1
            if 'replies' in comment['data']:
                process_comments(comment['data']['replies'], comment_counter)

def get_top_users(subreddit_url: str, token: str, time_period: int = 3, limit: int = 3): # TODO: Add annotation for output
    post_counter: Counter[str] = Counter()
    comment_counter: Counter[str] = Counter()
    params = {'t': 'all', 'limit': 100}

    date_limit = get_date_limit(time_period)
    reached_date_limit = False
    counter = 0

    while counter < 10 and not reached_date_limit:
        response = make_authenticated_request(subreddit_url, token, params)

        for item in response['data']['children']:
            post = item['data']
            post_created_date = convert_unix_timestamp(post['created'])
            if post_created_date < date_limit:
                reached_date_limit = True
                break
            else:
                post_counter[post['author']] += 1
                permalink = post['permalink']
                comments_url = f'{REDDIT_OAUTH_URL}{permalink}.json'
                comments_response = make_authenticated_request(comments_url, token)
                process_comments(comments_response[1], comment_counter)

        params['after'] = response['data']['after']
        counter += 1

    top_posters = post_counter.most_common(limit)
    top_commenters = comment_counter.most_common(limit)
    return top_posters, top_commenters


