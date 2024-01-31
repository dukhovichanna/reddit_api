import pytest
from reddit_api.top_users import (
    get_date_limit,
    create_subreddit_url,
    get_top_authors_with_count,
    extract_posts_from_response,
    extract_comments_from_response,
    get_posts,
    get_comments
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
    assert top_commenters == [('Jane', 15), ('Jack', 3), ('John', 2)]


def test__extract_posts_from_response__return_list_of_posts(regular_post_response):
    result = extract_posts_from_response(regular_post_response)
    expected = [
        Post(
            author="throwawayhelp62525",
            created=datetime(2024, 1, 21, 22, 28, 42, tzinfo=timezone.utc),
            permalink="/r/books/comments/19cfrzw/my_comment/"
        )
    ]
    assert result == expected


def test__get_posts__assert_post_list_length(
        mocker,
        reddit_client,
        regular_post_response,
        response_with_post_outside_timelimit):

    mocker.patch.object(reddit_client, 'make_authenticated_request', side_effect=[
        regular_post_response,
        regular_post_response,
        response_with_post_outside_timelimit
        ])
    date_limit = datetime(2023, 1, 26, tzinfo=timezone.utc)
    subreddit_url = 'https://oauth.reddit.com/r/test/new'

    posts = get_posts(reddit_client, date_limit, subreddit_url)

    assert len(posts) == 2


def test__get_posts__assert_last_post_within_time_limit(
        mocker,
        reddit_client,
        regular_post_response,
        response_with_post_outside_timelimit):

    mocker.patch.object(reddit_client, 'make_authenticated_request', side_effect=[
        regular_post_response,
        regular_post_response,
        response_with_post_outside_timelimit
        ])
    date_limit = datetime(2023, 1, 26, tzinfo=timezone.utc)
    subreddit_url = 'https://oauth.reddit.com/r/test/new'

    posts = get_posts(reddit_client, date_limit, subreddit_url)

    assert posts[-1].created >= date_limit


def test__extract_comments_from_response__assert_comment_response_with_2_items_yields_2_comments(comment_data):
    comments_list = []
    extract_comments_from_response(comment_data, comments_list)

    assert len(comments_list) == 2


def test__extract_comments_from_response__assert_author_on_1st_comment(comment_data):
    comments_list = []
    extract_comments_from_response(comment_data, comments_list)
    assert comments_list[0].author == 'user1'


def test__extract_comments_from_response__assert_permalink_on_2nd_comment(comment_data):
    comments_list = []
    extract_comments_from_response(comment_data, comments_list)
    assert comments_list[1].permalink == '/r/books/comments/2/'


def test__extract_comments_from_response__assert_len_with_nested_comments(
        comment_data_with_nested_replies):
    comments_list = []
    extract_comments_from_response(comment_data_with_nested_replies, comments_list)
    assert len(comments_list) == 3


def test__extract_comments_from_response__assert_parent_comment_has_replies(
        comment_data_with_nested_replies):
    comments_list = []
    extract_comments_from_response(comment_data_with_nested_replies, comments_list)
    assert comments_list[0].replies is not None


def test__extract_comments_from_response__assert_3_comment_author(
        comment_data_with_nested_replies):
    comments_list = []
    extract_comments_from_response(comment_data_with_nested_replies, comments_list)
    assert comments_list[2].author == 'user2'


def test__get_comments__empty_post_list_return_empty_comment_list(reddit_client):
    empty_posts_list = []
    list_of_comments = get_comments(empty_posts_list, reddit_client)
    assert len(list_of_comments) == 0


