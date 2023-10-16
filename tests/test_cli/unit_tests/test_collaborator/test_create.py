import pytest
from epicevents.data_access_layer.collaborator import Collaborator
from epicevents.cli.collaborator import create, _memorize_token, _verify_token
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError


def test_creation_successful(monkey_dotenv, valid_token, capsys):
    _memorize_token(valid_token)

    create(first_name="Collab",
           name="Test",
           email="collab@test.fr",
           password="Passtest",
           department=1)

    captured = capsys.readouterr()
    
    assert "a été créé avec succès." in captured.out.strip() 

def test_creation_token_fails(monkey_dotenv, wrong_token, capsys):
    with pytest.raises(InvalidTokenError):
        _memorize_token(wrong_token)
        
        create(first_name="Collab",
            name="Test",
            email="collabo@test.fr",
            password="Passtest",
            department=1)
    
def test_creation_not_allowed(monkey_dotenv, wrong_department_token, capsys):
    _memorize_token(wrong_department_token)
    
    create(first_name="Collab",
           name="Test",
           email="collab@test.fr",
           password="Passtest",
           department=1)

    captured = capsys.readouterr()
    
    assert "Action restreinte." in captured.out.strip()
    
def test_creation_expired_token(monkey_dotenv, expired_token, capsys):
    with pytest.raises(ExpiredSignatureError):
        _memorize_token(expired_token)
        
        create(first_name="Collab",
            name="Test",
            email="collabo@test.fr",
            password="Passtest",
            department=1)
