import pytest, jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from epicevents.cli import collaborator
from epicevents.cli.collaborator import _verify_token, _memorize_token

def test_verify_token(monkey_dotenv, valid_token):
    _memorize_token(valid_token)
    
    expected_result = (True, jwt.decode(valid_token, key=collaborator.SECRET_KEY, algorithms=["HS256"]))
    
    assert _verify_token() == expected_result

def test_verify_expired_token(monkey_dotenv, expired_token):
    _memorize_token(expired_token)

    with pytest.raises(ExpiredSignatureError):
        _verify_token()

def test_verify_wrong_token(monkey_dotenv, wrong_token):
    _memorize_token(wrong_token)

    with pytest.raises(InvalidTokenError):
        _verify_token()

def test_verify_wrong_token_is_str(monkey_dotenv, wrong_token_str):
    _memorize_token(wrong_token_str)

    with pytest.raises(InvalidTokenError):
        _verify_token()
