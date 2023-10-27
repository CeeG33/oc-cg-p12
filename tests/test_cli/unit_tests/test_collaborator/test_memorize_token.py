import pytest
from dotenv import get_key
from epicevents.cli.collaborator import _memorize_token


def test_memorize_token():
    """
    GIVEN a token to be memorized
    WHEN the _memorize_token function is called with the token
    THEN it should memorize the token successfully, and the token in the environment should match the provided token.
    """
    token = "my_test_token"

    _memorize_token(token)

    env_token = get_key(".env", "TOKEN")

    assert env_token == token
