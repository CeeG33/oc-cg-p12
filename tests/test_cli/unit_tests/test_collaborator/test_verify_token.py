import pytest
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from epicevents.cli import collaborator
from epicevents.cli.collaborator import _verify_token


def test_verify_token(monkey_dotenv, monkey_read_token_correct, valid_token):
    """
    GIVEN a valid token from the environment variable and a token verification function
    WHEN the token is verified
    THEN the function should return a tuple with the first element being True (indicating a successful verification) and the second element being the decoded token data.
    """
    expected_result = (
        True,
        jwt.decode(valid_token, key=collaborator.SECRET_KEY, algorithms=["HS256"]),
    )

    assert _verify_token() == expected_result


def test_verify_expired_token(monkey_dotenv, monkey_read_token_expired, capsys):
    """
    GIVEN an expired token from the environment variable and a token verification function
    WHEN the token is verified
    THEN an ExpiredSignatureError should be raised, and an error message should indicate that the token has expired, and reauthentication is required.
    """
    with pytest.raises(ExpiredSignatureError):
        _verify_token()

    captured = capsys.readouterr()

    assert "Token expiré, veuillez vous réauthentifier." in captured.out.strip()


def test_verify_wrong_token(monkey_dotenv, monkey_read_token_wrong, capsys):
    """
    GIVEN an invalid token from the environment variable and a token verification function
    WHEN the token is verified
    THEN an InvalidTokenError should be raised, and an error message should indicate that the token is not valid, and reauthentication is required.
    """
    with pytest.raises(InvalidTokenError):
        _verify_token()

    captured = capsys.readouterr()

    assert (
        "Le token n'est pas valide, veuillez vous réauthentifier."
        in captured.out.strip()
    )


def test_verify_wrong_token_is_str(monkey_dotenv, monkey_read_token_wrong_str, capsys):
    """
    GIVEN an invalid token of type str from the environment variable and a token verification function
    WHEN the token is verified
    THEN a ValueError should be raised, indicating an invalid token format.
    """
    with pytest.raises(ValueError):
        _verify_token()
