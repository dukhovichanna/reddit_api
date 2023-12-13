from dataclasses import dataclass
import os

@dataclass
class Config:
    username: str

def load_from_env():
    return Config(
        username=os.environ['REDDIT_USERNAME'],
    )

config = load_from_env()