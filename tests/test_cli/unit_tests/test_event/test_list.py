import pytest
from epicevents.cli.collaborator import _memorize_token
from epicevents.cli.event import list
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError


def test_list_successful(valid_token, fake_event, capsys):
    _memorize_token(valid_token)
    list()

    captured = capsys.readouterr()
    
    assert "[ID]" in captured.out.strip() 

def test_list_token_fails(fake_event, wrong_token):
    with pytest.raises(InvalidTokenError):
        _memorize_token(wrong_token)
        list()
    
def test_list_token_expired(expired_token, fake_event):
    with pytest.raises(ExpiredSignatureError):
        _memorize_token(expired_token)
        list()
    
