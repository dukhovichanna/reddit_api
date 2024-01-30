from reddit_api.reddit_client import RedditClient
from reddit_api.config import config
from reddit_api.top_users import (
    create_subreddit_url,
    get_posts,
    get_date_limit,
    get_top_authors_with_count,
    get_comments)
import logging
import time

logger = logging.getLogger(__name__)


def main() -> None:
    logging.basicConfig(level=logging.DEBUG)

    reddit_client = RedditClient(
        client_id=config.client_id,
        client_secret=config.secret,
        username=config.username,
        password=config.password,
        user_agent=config.user_agent,
        api_url=config.api_url
    )

    subreddit_name = 'books'
    subreddit_url = create_subreddit_url(subreddit_name)
    date_limit = get_date_limit(3)

    while True:
        posts = get_posts(
            reddit_client=reddit_client,
            date_limit=date_limit,
            subreddit_url=subreddit_url
        )
        top_post_authors = get_top_authors_with_count(posts)
        list_of_comments = get_comments(posts, reddit_client)

        top_comment_authors = get_top_authors_with_count(list_of_comments)
        logger.info("Top Posters: %s", top_post_authors)
        logger.info("Top Commenters: %s", top_comment_authors)
        logger.info('Done.')

        time.sleep(config.timeout)


if __name__ == "__main__":
    main()
