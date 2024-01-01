from reddit_api.config import config
from reddit_api.top_users import create_subreddit_url, get_token, get_top_users
import logging

logger = logging.getLogger(__name__)


def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    subreddit_name = 'books'
    subreddit_url = create_subreddit_url(subreddit_name)
    token = get_token(config.client_id, config.secret, config.username, config.password)
    top_posters, top_commenters = get_top_users(subreddit_url, token)
    logger.info("Top Posters: %s", top_posters)
    logger.info("Top Commenters: %s", top_commenters)


if __name__ == "__main__":
    main()
