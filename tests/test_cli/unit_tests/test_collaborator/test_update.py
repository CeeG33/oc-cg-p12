import pytest
from typer import Exit
from argon2 import PasswordHasher
from peewee import DoesNotExist
from epicevents.data_access_layer.collaborator import Collaborator
from epicevents.cli.collaborator import update, _memorize_token
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

ph = PasswordHasher()

def test_first_name_update_successful(monkey_capture_message_collaborator, monkey_token_check_management, fake_collaborator_management, capsys):
    collaborator = fake_collaborator_management
    update(collaborator.id, "Gérard", first_name=True)

    updated_collaborator = Collaborator.get(Collaborator.id == collaborator.id)
    
    captured = capsys.readouterr()
    
    assert updated_collaborator.first_name == "Gérard"
    assert f"Le champ 'Prénom' du collaborateur n°{collaborator.id} a été mis à jour avec succès." in captured.out.strip()
    
def test_first_name_update_unsuccessful(monkey_capture_message_collaborator, monkey_token_check_management, fake_collaborator_management, capsys):
    collaborator = fake_collaborator_management
    with pytest.raises(ValueError):
        update(collaborator.id, "45644", first_name=True)

def test_name_update_successful(monkey_capture_message_collaborator, monkey_token_check_management, fake_collaborator_management, capsys):
    collaborator = fake_collaborator_management
    update(collaborator.id, "LEPETIT", name=True)

    updated_collaborator = Collaborator.get(Collaborator.id == collaborator.id)
    
    captured = capsys.readouterr()
    
    assert updated_collaborator.name == "LEPETIT"
    assert f"Le champ 'Nom' du collaborateur n°{collaborator.id} a été mis à jour avec succès." in captured.out.strip()

def test_name_update_unsuccessful(monkey_capture_message_collaborator, monkey_token_check_management, fake_collaborator_management, capsys):
    collaborator = fake_collaborator_management
    with pytest.raises(ValueError):
        update(collaborator.id, "45644", name=True)

def test_email_update_successful(monkey_capture_message_collaborator, monkey_token_check_management, fake_collaborator_management, capsys):
    collaborator = fake_collaborator_management
    update(collaborator.id, "nouveau@mail.com", email=True)

    updated_collaborator = Collaborator.get(Collaborator.id == collaborator.id)
    
    captured = capsys.readouterr()
    
    assert updated_collaborator.email == "nouveau@mail.com"
    assert f"Le champ 'Email' du collaborateur n°{collaborator.id} a été mis à jour avec succès." in captured.out.strip()

def test_email_update_unsuccessful(monkey_capture_message_collaborator, monkey_token_check_management, fake_collaborator_management, capsys):
    collaborator = fake_collaborator_management
    
    with pytest.raises(ValueError):
        update(collaborator.id, "aeraer", email=True)

def test_password_update_successful(monkey_capture_message_collaborator, monkey_token_check_management, fake_collaborator_management, capsys):
    collaborator = fake_collaborator_management
    update(collaborator.id, "Passtest", password=True)

    updated_collaborator = Collaborator.get(Collaborator.id == collaborator.id)
    
    captured = capsys.readouterr()
    
    assert ph.verify(updated_collaborator.password, "Passtest") == True
    assert f"Le champ 'Mot de passe' du collaborateur n°{collaborator.id} a été mis à jour avec succès." in captured.out.strip()

def test_department_update_successful(monkey_capture_message_collaborator, monkey_token_check_management, fake_collaborator_management, fake_department_management, capsys):
    collaborator = fake_collaborator_management
    update(collaborator.id, 1, department=True)

    updated_collaborator = Collaborator.get(Collaborator.id == collaborator.id)
    
    captured = capsys.readouterr()
    
    assert updated_collaborator.department.id == 1
    assert f"Le champ 'Département' du collaborateur n°{collaborator.id} a été mis à jour avec succès." in captured.out.strip()

def test_department_update_unsuccessful(monkey_capture_message_collaborator, monkey_token_check_management, fake_collaborator_management, capsys):
    collaborator = fake_collaborator_management
    
    with pytest.raises(Exit):
        update(collaborator.id, "10", department=True)
    
    captured = capsys.readouterr()
    
    assert "Veuillez entrer un numéro de département valide." in captured.out.strip()
    
def test_collaborator_update_fails_without_attributes(monkey_capture_message_collaborator, monkey_token_check_management, fake_collaborator_management, capsys):
    collaborator = fake_collaborator_management
    
    with pytest.raises(Exit):
        update(collaborator.id, "10")
    
    captured = capsys.readouterr()
    
    assert "Vous n'avez pas sélectionné d'attribut à modifier." in captured.out.strip()
    
def test_collaborator_update_fails_with_wrong_collaborator_id(monkey_capture_message_collaborator, monkey_token_check_management, capsys):
    fake_id = -100
    
    update(fake_id, "Gérard", first_name=True)
    
    captured = capsys.readouterr()
    
    assert f"Aucun collaborateur trouvé avec l'ID n°{fake_id}." in captured.out.strip()
    
def test_collaborator_update_not_authorized(monkey_capture_message_collaborator, monkey_token_check_correct_sales, fake_collaborator_management, capsys):
    collaborator = fake_collaborator_management
    
    with pytest.raises(Exit):
        update(collaborator.id, "Gérard", first_name=True)
    
    captured = capsys.readouterr()
    
    assert "Action restreinte." in captured.out.strip()
    
def test_collaborator_update_fails_without_authentication(monkey_capture_message_collaborator, monkey_token_check_false, fake_collaborator_management, capsys):
    collaborator = fake_collaborator_management
    
    with pytest.raises(Exit):
        update(collaborator.id, "Gérard", first_name=True)
    
    captured = capsys.readouterr()
    
    assert "Veuillez vous authentifier et réessayer." in captured.out.strip()
