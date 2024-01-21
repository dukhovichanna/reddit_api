from reddit_api.reddit_client import RedditClient
from reddit_api.models import Post, Comment, Response
from reddit_api.errors import InvalidSubredditNameError
from datetime import datetime, timedelta, timezone
from collections import Counter
from typing import List, Dict, Any
import re
import logging


logger = logging.getLogger(__name__)


def get_date_limit(limit_in_days: int) -> datetime:
    if limit_in_days < 0:
        raise ValueError("The limit_in_days argument must be a non-negative integer.")
    return datetime.now(timezone.utc) - timedelta(days=limit_in_days)


def create_subreddit_url(subreddit_name: str) -> str:
    if not re.match("^[a-zA-Z0-9_]+$", subreddit_name):
        raise InvalidSubredditNameError()
    return f'https://oauth.reddit.com/r/{subreddit_name}/new'


def extract_posts(response: Response) -> List[Post]:
    return [Post(**item['data']) for item in response.children]


def get_posts(reddit_client: RedditClient, date_limit: datetime, subreddit_url: str) -> List[Post]:
    reached_date_limit = False
    list_of_posts = []
    params = {'t': 'all', 'limit': 100}

    while not reached_date_limit:
        response = reddit_client.make_authenticated_request(subreddit_url, params)
        posts = extract_posts(response)
        for post in posts:
            if post.created < date_limit:
                reached_date_limit = True
                break
            else:
                list_of_posts.append(post)
        params['after'] = response.after

    return list_of_posts


def process_comments(comment_data: List[Dict[str, Any]], comments_list: List[Comment]) -> None:
    for comment_info in comment_data:
        if 'author' in comment_info['data']:
            comment = Comment(**comment_info['data'])
            comments_list.append(comment)
            if comment.replies:
                process_comments(comment.replies['data']['children'], comments_list)


def get_comments(posts: List[Post], reddit_client: RedditClient) -> List[Comment]:
    list_of_comments: List[Comment] = []
    count = 1
    for post in posts:
        comments_response = reddit_client.make_authenticated_request(post.comments_url)
        process_comments(comments_response.children, list_of_comments)
        logger.info("Processed %s post out of %s", count, len(posts))
        count += 1
    return list_of_comments


def get_top_authors_with_count(
        comments:  List[Post] | List[Comment],
        top_n: int = 3) -> List[tuple]:
    author_counts = Counter(comment.author for comment in comments)
    top_authors = author_counts.most_common(top_n)
    return top_authors
