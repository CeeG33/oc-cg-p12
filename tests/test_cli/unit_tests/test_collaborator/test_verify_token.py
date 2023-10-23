import pytest, jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from epicevents.cli import collaborator
from epicevents.cli.collaborator import _verify_token, _memorize_token

def test_verify_token(monkey_dotenv, monkey_read_token_correct, valid_token):
    expected_result = (True, jwt.decode(valid_token, key=collaborator.SECRET_KEY, algorithms=["HS256"]))
    
    assert _verify_token() == expected_result

def test_verify_expired_token(monkey_dotenv, monkey_read_token_expired, capsys):
    with pytest.raises(ExpiredSignatureError):
        _verify_token()
    
    captured = capsys.readouterr()
    
    assert "Token expiré, veuillez vous réauthentifier." in captured.out.strip()

def test_verify_wrong_token(monkey_dotenv, monkey_read_token_wrong, capsys):
    with pytest.raises(InvalidTokenError):
        _verify_token()
        
    captured = capsys.readouterr()
    
    assert "Le token n'est pas valide, veuillez vous réauthentifier." in captured.out.strip()

def test_verify_wrong_token_is_str(monkey_dotenv, monkey_read_token_wrong_str, capsys):
    with pytest.raises(ValueError):
        _verify_token()

