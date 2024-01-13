from reddit_api.reddit_client import RedditClient
from reddit_api.config import config
from reddit_api.top_users import create_subreddit_url, get_top_users
import logging

logger = logging.getLogger(__name__)


def main() -> None:
    logging.basicConfig(level=logging.DEBUG)

    reddit_client = RedditClient(
        client_id=config.client_id,
        client_secret=config.secret,
        username=config.username,
        password=config.password,
        user_agent=config.user_agent
    )

    subreddit_name = 'books'
    subreddit_url = create_subreddit_url(subreddit_name)
    top_posters, top_commenters = get_top_users(subreddit_url, reddit_client)
    logger.info("Top Posters: %s", top_posters)
    logger.info("Top Commenters: %s", top_commenters)


if __name__ == "__main__":
    main()
