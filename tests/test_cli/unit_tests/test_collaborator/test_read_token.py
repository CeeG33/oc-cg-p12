import pytest
from dotenv import set_key
from epicevents.cli.collaborator import _read_token


def test_read_token():
    """
    GIVEN a token stored in the environment
    WHEN the _read_token function is called
    THEN it should successfully read and return the stored token.
    """
    set_key(".env", "TOKEN", "my_token")
    assert _read_token() == "my_token"
