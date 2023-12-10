import settings
from datetime import datetime, timedelta
from collections import Counter
import requests

url = 'https://oauth.reddit.com/r/books/new'

def get_token(client_id, client_secret, username, password):
    url = "https://www.reddit.com/api/v1/access_token"
    headers = {"User-Agent": settings.USER_AGENT}
    data = {
        "grant_type": "password",
        "username": username,
        "password": password
    }
    auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    response = requests.post(url, data=data, headers=headers, auth=auth)
    token = response.json().get("access_token")
    return token

def make_authenticated_request(url, token, params=None):
    headers = {"User-Agent": settings.USER_AGENT, "Authorization": f"bearer {token}"}
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def convert_unix_timestamp(ts):
    return datetime.utcfromtimestamp(ts)

def get_date_limit(limit_in_days):
    return datetime.today() - timedelta(days=limit_in_days)

def get_top_users(subreddit_url, token, time_period=3, limit=3):
    post_counter = Counter()
    
    # Initial request
    params = {'t': 'all', 'limit': 100}
    response = make_authenticated_request(subreddit_url, token, params)
    
    # Set date limit
    date_limit = get_date_limit(time_period)
    reached_date_limit = False
    counter = 0
    
    while counter < 2 and not reached_date_limit:
        for item in response['data']['children']:
            post = item['data']
            post_created_date = convert_unix_timestamp(post['created'])
            if post_created_date < date_limit:
                reached_date_limit = True
                break
            else:
                post_counter[post['author']] += 1
        
        # Set the 'after' parameter for the next request to get the next batch of posts
        params['after'] = response['data']['after']        
        response = make_authenticated_request(subreddit_url, token, params)                  
        counter +=1
        
    top_posters = post_counter.most_common(limit)
    
    return top_posters

token = get_token(settings.CLIENT_ID, settings.SECRET, settings.USERNAME, settings.PASSWORD)

print(get_top_users(url, token))






