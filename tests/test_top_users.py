import pytest
from reddit_api.top_users import (
    convert_unix_timestamp,
    get_date_limit,
    create_subreddit_url,
    construct_params
)
from reddit_api.errors import InvalidSubredditNameError
from datetime import datetime, timedelta


@pytest.mark.parametrize(
    "timestamp, expected_result",
    [
        (1702340475.0, datetime(2023, 12, 12, 0, 21, 15)),
        (1.0, datetime(1970, 1, 1, 0, 0, 1)),
        (2000000000.0, datetime(2033, 5, 18, 3, 33, 20)),
        (1703980800.0, datetime(2023, 12, 31, 0, 0, 0)),
    ],
)
def test__convert_unix_timestamp_into_utc_datetime(timestamp, expected_result):
    result = convert_unix_timestamp(timestamp)
    assert result == expected_result

def test__get_date_limit__positive_number_input():
    assert get_date_limit(7) == datetime.today() - timedelta(days=7)

def test__get_date_limit__allow_zero_as_input():
    assert get_date_limit(0) == datetime.today()

def test__get_date_limit_raise_error_when_negative_input():
    limit_in_days = -7
    with pytest.raises(ValueError, 
                       match="The limit_in_days argument must be a non-negative integer."):
        get_date_limit(limit_in_days)

def test__create_subreddit_url__allow_basic_alpha_name_without_digits():
    subreddit_name = 'portlandme'
    result = create_subreddit_url(subreddit_name)
    expected_result = f'https://oauth.reddit.com/r/{subreddit_name}/new'
    assert result == expected_result

def test__create_subreddit_url__allow_alpha_numeric_name():
    subreddit_name = '2007scape'
    result = create_subreddit_url(subreddit_name)
    expected_result = f'https://oauth.reddit.com/r/{subreddit_name}/new'
    assert result == expected_result

def test__create_subreddit_url__allow_alpha_numeric_name_with_underscore():
    subreddit_name = 'internal_arts'
    result = create_subreddit_url(subreddit_name)
    expected_result = f'https://oauth.reddit.com/r/{subreddit_name}/new'
    assert result == expected_result

def test__create_subreddit_url__raise_error_when_spaces_in_name():
    subreddit_name = 'portland me'
    with pytest.raises(InvalidSubredditNameError, 
                       match="Subreddit name must only contain alphanumeric characters and underscores."):
        create_subreddit_url(subreddit_name)

def test__create_subreddit_url__raise_error_when_special_characters_in_name():
    subreddit_name = 'portlandme123!@#'
    with pytest.raises(InvalidSubredditNameError, 
                       match="Subreddit name must only contain alphanumeric characters and underscores."):
        create_subreddit_url(subreddit_name)

def test__construct_params__valid_input():
    result = construct_params(time_period=7, num_posts_per_page=50)
    assert result == {'t': 'all', 'limit': '50', 'time_period': 7}

def test__construct_params__default_num_posts():
    result = construct_params(time_period=30)
    assert result == {'t': 'all', 'limit': '100', 'time_period': 30}

def test__construct_params__raise_error_when_invalid_time_period():
    with pytest.raises(ValueError, match="The time_period argument must be a non-negative integer."):
        construct_params(time_period=-1, num_posts_per_page=50)

def test__construct_params__raise_error_when_invalid_num_posts():
    with pytest.raises(ValueError, match="The num_posts argument must be a positive integer."):
        construct_params(time_period=7, num_posts_per_page=0)
