import pytest, jwt, os
from dotenv import load_dotenv, find_dotenv
from epicevents.cli import collaborator
from epicevents.cli.collaborator import _memorize_token


def test_memorize_token(monkey_dotenv):
    token = "my_test_token"
    _memorize_token(token)
    env_token = os.getenv("TOKEN")
    
    assert env_token == token
