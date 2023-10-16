import pytest
from epicevents.data_access_layer.collaborator import Collaborator
from epicevents.cli.collaborator import list, _memorize_token, _verify_token
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError


def test_list_successful(monkey_dotenv, valid_token, capsys):
    _memorize_token(valid_token)
    
    list()

    captured = capsys.readouterr()
    
    assert "[ID]" in captured.out.strip() 

def test_list_token_fails(monkey_dotenv, wrong_token, capsys):
    with pytest.raises(InvalidTokenError):
        _memorize_token(wrong_token)
        list()
    
def test_list_wrong_department(monkey_dotenv, fake_department, wrong_department_token, capsys):
    _memorize_token(wrong_department_token)
    
    list()

    captured = capsys.readouterr()
    
    assert "Action restreinte." in captured.out.strip()
    
def test_list_token_expired(monkey_dotenv, expired_token, fake_department, capsys):
    with pytest.raises(ExpiredSignatureError):
        _memorize_token(expired_token)
        
        list()
    
