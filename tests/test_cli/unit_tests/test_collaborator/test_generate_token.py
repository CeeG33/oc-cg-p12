import pytest
import jwt
from epicevents.cli import collaborator
from epicevents.cli.collaborator import _generate_token


def test_generate_token(fake_collaborator_management, fake_department_management):
    """
    GIVEN a management collaborator and a management department
    WHEN the _generate_token function is called with the management collaborator
    THEN it should generate a token using the collaborator's data and the specified SECRET_KEY and algorithm (HS256),
    and the generated token should match the expected result.
    """
    expected_result = jwt.encode(
        fake_collaborator_management.get_data(),
        key=collaborator.SECRET_KEY,
        algorithm="HS256",
    )

    assert _generate_token(fake_collaborator_management) == expected_result
