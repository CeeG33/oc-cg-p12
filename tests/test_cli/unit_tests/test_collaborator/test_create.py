import pytest
from typer import Exit
from epicevents.data_access_layer.collaborator import Collaborator
from epicevents.cli.collaborator import create, _memorize_token, _verify_token
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError


def test_creation_successful(monkey_token_check_management, capsys):
    create(first_name="Collab",
           name="Test",
           email="collab@test.fr",
           password="Passtest",
           department=1)

    captured = capsys.readouterr()
    
    assert "a été créé avec succès." in captured.out.strip() 

def test_creation_not_authorized(monkey_token_check_fake_sales, capsys):
    with pytest.raises(Exit):
        
        create(first_name="Collab",
            name="Test",
            email="collabo@test.fr",
            password="Passtest",
            department=1)
    
def test_creation_not_allowed(monkey_token_check_fake_sales, capsys):
    with pytest.raises(Exit):
        create(first_name="Collab",
            name="Test",
            email="collab@test.fr",
            password="Passtest",
            department=1)

    captured = capsys.readouterr()
    
    assert "Action restreinte." in captured.out.strip()
    
def test_creation_token_fails(monkey_token_check_false, capsys):
    with pytest.raises(Exit):
        
        create(first_name="Collab",
            name="Test",
            email="collabo@test.fr",
            password="Passtest",
            department=1)
        
    captured = capsys.readouterr()
    
    assert "Veuillez vous authentifier et réessayer." in captured.out.strip()
    
