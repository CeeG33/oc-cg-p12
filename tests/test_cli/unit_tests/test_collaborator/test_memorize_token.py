import pytest, os
from dotenv import get_key
from epicevents.cli.collaborator import _memorize_token


def test_memorize_token():
    token = "my_test_token"
    
    _memorize_token(token)
    
    env_token = get_key(".env", "TOKEN")

    assert env_token == token
