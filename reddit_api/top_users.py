import settings
from datetime import datetime, timedelta
from collections import Counter
import requests

REDDIT_API_URL = 'https://www.reddit.com/api/v1/access_token'
REDDIT_OAUTH_URL = 'https://oauth.reddit.com'

def get_token(client_id: str, client_secret: str, username: str, password: str) -> str:
    headers = {"User-Agent": settings.USER_AGENT}
    data = {
        "grant_type": "password",
        "username": username,
        "password": password
    }
    auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    response = requests.post(REDDIT_API_URL, data=data, headers=headers, auth=auth)
    return response.json()["access_token"]

def make_authenticated_request(url: str, token: str, params=None): # TODO: Add annotiation to params and output
    headers = {"User-Agent": settings.USER_AGENT, "Authorization": f"bearer {token}"}
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def convert_unix_timestamp(ts: float) -> datetime:
    return datetime.utcfromtimestamp(ts)

def get_date_limit(limit_in_days: int) -> datetime:
    return datetime.today() - timedelta(days=limit_in_days)

def create_subreddit_url(subreddit_name: str) -> str:
    return f'{REDDIT_OAUTH_URL}/r/{subreddit_name}/new'

def get_top_users(subreddit_url: str, token: str, time_period: int = 3, limit: int = 3): # TODO: Add annotation for output
    post_counter = Counter()
    params = {'t': 'all', 'limit': 100}

    date_limit = get_date_limit(time_period)
    reached_date_limit = False
    counter = 0

    while counter < 10 and not reached_date_limit:
        response = make_authenticated_request(subreddit_url, token, params)

        for item in response['data']['children']:
            post = item['data']
            post_created_date = convert_unix_timestamp(post['created'])

            if post_created_date < date_limit:
                reached_date_limit = True
                break
            else:
                post_counter[post['author']] += 1

        params['after'] = response['data']['after']
        counter += 1

    top_posters = post_counter.most_common(limit)
    return top_posters

# Example usage
subreddit_name = 'books'
subreddit_url = create_subreddit_url(subreddit_name)
token = get_token(settings.CLIENT_ID, settings.SECRET, settings.USERNAME, settings.PASSWORD)
top_users = get_top_users(subreddit_url, token)
print(top_users)