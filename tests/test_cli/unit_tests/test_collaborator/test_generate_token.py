import pytest, jwt
from epicevents.cli import collaborator
from epicevents.cli.collaborator import _generate_token

def test_generate_token(fake_collaborator):
    expected_result = jwt.encode(fake_collaborator.get_data(), key=collaborator.SECRET_KEY, algorithm="HS256")
    
    assert _generate_token(fake_collaborator) == expected_result