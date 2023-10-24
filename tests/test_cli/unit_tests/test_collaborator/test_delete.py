import pytest
from typer import Exit
from argon2 import PasswordHasher
from peewee import DoesNotExist
from epicevents.data_access_layer.collaborator import Collaborator
from epicevents.cli.collaborator import delete, _memorize_token
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

ph = PasswordHasher()

def test_collaborator_delete_successful(monkey_capture_message_collaborator, monkey_token_check_management, fake_collaborator_management, capsys):
    collaborator = fake_collaborator_management
    delete(collaborator.id)

    updated_collaborator = Collaborator.get_or_none(Collaborator.id == collaborator.id)
    
    captured = capsys.readouterr()
    
    assert updated_collaborator == None
    assert f"Le collaborateur n°{collaborator.id} a été supprimé avec succès." in captured.out.strip()
    
def test_collaborator_deletion_fails_with_wrong_collaborator_id(monkey_token_check_management, capsys):
    fake_id = -100
    
    delete(fake_id)
    
    captured = capsys.readouterr()
    
    assert f"Aucun collaborateur trouvé avec l'ID n°{fake_id}." in captured.out.strip()
    
def test_collaborator_deletion_not_authorized(monkey_token_check_correct_sales, fake_collaborator_management, capsys):
    collaborator = fake_collaborator_management
    
    with pytest.raises(Exit):
        delete(collaborator.id)
    
    captured = capsys.readouterr()
    
    assert "Action restreinte." in captured.out.strip()
    
def test_collaborator_deletion_fails_without_authentication(monkey_token_check_false, fake_collaborator_management, capsys):
    collaborator = fake_collaborator_management
    
    with pytest.raises(Exit):
        delete(collaborator.id)
    
    captured = capsys.readouterr()
    
    assert "Veuillez vous authentifier et réessayer." in captured.out.strip()
