class InvalidSubredditNameError(Exception):
    def __init__(self):
        self.message = "Subreddit name must only contain alphanumeric characters and underscores."
        super().__init__(self.message)
