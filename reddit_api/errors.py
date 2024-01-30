class InvalidSubredditNameError(Exception):
    def __init__(self) -> None:
        self.message = (
            "Subreddit name must only contain alphanumeric characters and underscores."
        )
        super().__init__(self.message)


class RedditClientError(Exception):
    def __init__(self, reason: str) -> None:
        self.reason = reason
        super().__init__(reason)


class RedditAuthenticationError(RedditClientError):
    def __init__(self) -> None:
        super().__init__("Authentication failed. Invalid token or credentials.")


class RedditTimeoutError(RedditClientError):
    def __init__(self) -> None:
        super().__init__("Request timed out.")
