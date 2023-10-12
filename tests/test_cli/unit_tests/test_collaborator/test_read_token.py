import pytest, jwt, os
from epicevents.cli import collaborator
from epicevents.cli.collaborator import _read_token

def test_read_token(monkey_dotenv):
    os.environ["TOKEN"] = "my_token"
    assert _read_token() == "my_token"