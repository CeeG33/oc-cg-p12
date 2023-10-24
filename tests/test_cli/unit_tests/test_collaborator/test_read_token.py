import pytest, os
from dotenv import set_key, get_key
from epicevents.cli.collaborator import _read_token


def test_read_token():
    set_key(".env", "TOKEN", "my_token")
    assert _read_token() == "my_token"
