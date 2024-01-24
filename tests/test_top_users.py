import pytest
from reddit_api.top_users import (
    get_date_limit,
    create_subreddit_url,
    get_top_authors_with_count,
    extract_posts_from_response
)
from reddit_api.models import Post
from reddit_api.errors import InvalidSubredditNameError
from datetime import datetime, timedelta, timezone


def test__get_date_limit__positive_number_input():
    result = get_date_limit(7).replace(microsecond=0)
    expected = datetime.now(timezone.utc).replace(microsecond=0) - timedelta(days=7)
    assert result == expected

def test__get_date_limit__allow_zero_as_input():
    result = get_date_limit(0).replace(microsecond=0)
    expected = datetime.now(timezone.utc).replace(microsecond=0)
    assert result == expected


def test__get_date_limit_raise_error_when_negative_input():
    limit_in_days = -7
    with pytest.raises(ValueError):
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
    with pytest.raises(InvalidSubredditNameError):
        create_subreddit_url(subreddit_name)


def test__create_subreddit_url__raise_error_when_special_characters_in_name():
    subreddit_name = 'portlandme123!@#'
    with pytest.raises(InvalidSubredditNameError):
        create_subreddit_url(subreddit_name)


def test__get_top_authors_with_count__top_commenters(list_of_comments):
    top_commenters = get_top_authors_with_count(list_of_comments)
    assert top_commenters == [('Jane', 15),('Jack', 3),('John', 2)]


def test__extract_posts_from_response__return_list_of_posts(post_response):
    result = extract_posts_from_response(post_response)
    expected = [
        Post(
            author="throwawayhelp62525",
            created=datetime(2024, 1, 21, 22, 28, 42, tzinfo=timezone.utc),
            permalink="/r/books/comments/19cfrzw/is_it_me_or_is_dark_matter_by_blake_crouch_tooblah/"
        )
    ]
    assert result == expected
