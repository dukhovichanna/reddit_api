import pytest
import reddit_api.settings
from reddit_api.top_users import convert_unix_timestamp
from datetime import datetime


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
