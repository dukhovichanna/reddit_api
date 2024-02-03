
def test__comment__convert_empty_string_to_none(make_comment):
    comment_with_empty_replies = make_comment()
    assert comment_with_empty_replies.replies is None

def test__comment__assert_non_empty_replies(make_comment):
    replies = {"data": {"after": "a1s2d3f4", "children": [1, 2]}}
    comment_with_empty_replies = make_comment(replies=replies)
    assert comment_with_empty_replies.replies == replies
