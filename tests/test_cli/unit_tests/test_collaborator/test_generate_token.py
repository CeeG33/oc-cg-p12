import pytest, jwt
from epicevents.cli import collaborator
from epicevents.cli.collaborator import _generate_token


def test_generate_token(fake_collaborator_management, fake_department_management):
    expected_result = jwt.encode(
        fake_collaborator_management.get_data(),
        key=collaborator.SECRET_KEY,
        algorithm="HS256",
    )

    assert _generate_token(fake_collaborator_management) == expected_result
