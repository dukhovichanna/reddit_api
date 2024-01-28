class InvalidSubredditNameError(Exception):
    def __init__(self) -> None:
        self.message = (
            "Subreddit name must only contain alphanumeric characters and underscores."
        )
        super().__init__(self.message)


class RedditAuthenticationError(Exception):
    def __init__(self) -> None:
        self.message = ("Authentication failed. Invalid token or credentials.")
        super().__init__(self.message)


class RedditTimeoutError(Exception):
    def __init__(self) -> None:
        self.message = ("Request timed out.")
        super().__init__(self.message)
