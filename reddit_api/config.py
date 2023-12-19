from dataclasses import dataclass
import os

@dataclass
class Config:
    username: str
    password: str
    secret: str
    client_id: str
    client_name: str
    user_agent: str

def load_from_env() -> Config:
    return Config(
        username=os.environ['REDDIT_USERNAME'],
        password=os.environ['REDDIT_PASSWORD'],
        secret=os.environ['REDDIT_SECRET'],
        client_id=os.environ['REDDIT_CLIENT_ID'],
        client_name=os.environ['REDDIT_CLIENT_NAME'],
        user_agent=os.environ['REDDIT_USER_AGENT']
    )

config = load_from_env()