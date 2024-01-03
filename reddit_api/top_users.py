from reddit_api.reddit_client import RedditClient
from reddit_api.errors import InvalidSubredditNameError
from datetime import datetime, timedelta
from collections import Counter
from dataclasses import dataclass
from typing import Dict, Any, List, Tuple
import re
import logging

REDDIT_OAUTH_URL = 'https://oauth.reddit.com'

logger = logging.getLogger(__name__)


@dataclass
class Post:
    author: str
    created: datetime
    comments_url: str


def convert_unix_timestamp(unix_timestamp: float) -> datetime:
    return datetime.utcfromtimestamp(unix_timestamp)


def get_date_limit(limit_in_days: int) -> datetime:
    if limit_in_days < 0:
        raise ValueError("The limit_in_days argument must be a non-negative integer.")
    return datetime.today() - timedelta(days=limit_in_days)


def create_subreddit_url(subreddit_name: str) -> str:
    if not re.match("^[a-zA-Z0-9_]+$", subreddit_name):
        raise InvalidSubredditNameError()
    return f'https://oauth.reddit.com/r/{subreddit_name}/new'


def process_comments(comment_data: Dict[str, Any], comment_counter: Counter) -> None:
    if 'data' in comment_data and 'children' in comment_data['data']:
        for comment in comment_data['data']['children']:
            if 'data' in comment and 'author' in comment['data']:
                comment_author = comment['data']['author']
                comment_counter[comment_author] += 1
            if 'replies' in comment['data']:
                process_comments(comment['data']['replies'], comment_counter)


def get_top_users(
        subreddit_url: str,
        reddit_client: RedditClient,
        time_period: int = 3,
        limit: int = 3) -> Tuple[List[Tuple[str, int]], List[Tuple[str, int]]]:
    post_counter: Counter[str] = Counter()
    comment_counter: Counter[str] = Counter()
    params = {'t': 'all', 'limit': 100}

    date_limit = get_date_limit(time_period)
    reached_date_limit = False
    counter = 0

    while counter < 10 and not reached_date_limit:
        response = reddit_client.make_authenticated_request(subreddit_url, params)

        for item in response['data']['children']:
            post = Post(
                author=item['data']['author'],
                created=convert_unix_timestamp(item['data']['created']),
                comments_url=f"{REDDIT_OAUTH_URL}{item['data']['permalink']}.json"
            )
            if post.created < date_limit:
                reached_date_limit = True
                break
            else:
                post_counter[post.author] += 1
                comments_response = reddit_client.make_authenticated_request(post.comments_url)
                process_comments(comments_response[1], comment_counter)

        params['after'] = response['data']['after']
        counter += 1

    top_posters = post_counter.most_common(limit)
    top_commenters = comment_counter.most_common(limit)
    return top_posters, top_commenters
