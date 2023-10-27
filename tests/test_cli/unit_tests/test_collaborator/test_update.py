import pytest
from typer import Exit
from argon2 import PasswordHasher
from epicevents.data_access_layer.collaborator import Collaborator
from epicevents.cli.collaborator import update

ph = PasswordHasher()


def test_first_name_update_successful(
    monkey_capture_message_collaborator,
    monkey_token_check_management,
    fake_collaborator_management,
    capsys,
):
    """
    GIVEN a collaborator and a new first name
    WHEN the update function is called to change the collaborator's first name
    THEN it should successfully update the first name of the collaborator.
    """
    collaborator = fake_collaborator_management
    update(collaborator.id, "Gérard", first_name=True)

    updated_collaborator = Collaborator.get(Collaborator.id == collaborator.id)

    captured = capsys.readouterr()

    assert updated_collaborator.first_name == "Gérard"
    assert (
        f"Le champ 'Prénom' du collaborateur n°{collaborator.id} a été mis à jour avec succès."
        in captured.out.strip()
    )


def test_first_name_update_unsuccessful(
    monkey_capture_message_collaborator,
    monkey_token_check_management,
    fake_collaborator_management,
    capsys,
):
    """
    GIVEN a collaborator and an invalid first name
    WHEN the update function is called to change the collaborator's first name
    THEN a ValueError should be raised, and an error message should indicate an invalid first name.
    """
    collaborator = fake_collaborator_management
    with pytest.raises(ValueError):
        update(collaborator.id, "45644", first_name=True)


def test_name_update_successful(
    monkey_capture_message_collaborator,
    monkey_token_check_management,
    fake_collaborator_management,
    capsys,
):
    """
    GIVEN a collaborator and a new last name
    WHEN the update function is called to change the collaborator's last name
    THEN the collaborator's last name should be successfully updated, and a success message should be printed.
    """
    collaborator = fake_collaborator_management
    update(collaborator.id, "LEPETIT", name=True)

    updated_collaborator = Collaborator.get(Collaborator.id == collaborator.id)

    captured = capsys.readouterr()

    assert updated_collaborator.name == "LEPETIT"
    assert (
        f"Le champ 'Nom' du collaborateur n°{collaborator.id} a été mis à jour avec succès."
        in captured.out.strip()
    )


def test_name_update_unsuccessful(
    monkey_capture_message_collaborator,
    monkey_token_check_management,
    fake_collaborator_management,
    capsys,
):
    """
    GIVEN a collaborator and an invalid last name
    WHEN the update function is called to change the collaborator's last name
    THEN a ValueError should be raised, and an error message should indicate an invalid last name.
    """
    collaborator = fake_collaborator_management
    with pytest.raises(ValueError):
        update(collaborator.id, "45644", name=True)


def test_email_update_successful(
    monkey_capture_message_collaborator,
    monkey_token_check_management,
    fake_collaborator_management,
    capsys,
):
    """
    GIVEN a collaborator and a new email address
    WHEN the update function is called to change the collaborator's email address
    THEN the collaborator's email address should be successfully updated, and a success message should be printed.
    """
    collaborator = fake_collaborator_management
    update(collaborator.id, "nouveau@mail.com", email=True)

    updated_collaborator = Collaborator.get(Collaborator.id == collaborator.id)

    captured = capsys.readouterr()

    assert updated_collaborator.email == "nouveau@mail.com"
    assert (
        f"Le champ 'Email' du collaborateur n°{collaborator.id} a été mis à jour avec succès."
        in captured.out.strip()
    )


def test_email_update_unsuccessful(
    monkey_capture_message_collaborator,
    monkey_token_check_management,
    fake_collaborator_management,
    capsys,
):
    """
    GIVEN a collaborator and an invalid email address
    WHEN the update function is called to change the collaborator's email address
    THEN a ValueError should be raised, and an error message should indicate an invalid email address.
    """
    collaborator = fake_collaborator_management

    with pytest.raises(ValueError):
        update(collaborator.id, "aeraer", email=True)


def test_password_update_successful(
    monkey_capture_message_collaborator,
    monkey_token_check_management,
    fake_collaborator_management,
    capsys,
):
    """
    GIVEN a collaborator and a new password
    WHEN the update function is called to change the collaborator's password
    THEN the collaborator's password should be successfully updated, and a success message should be printed.
    """
    collaborator = fake_collaborator_management
    update(collaborator.id, "Passtest", password=True)

    updated_collaborator = Collaborator.get(Collaborator.id == collaborator.id)

    captured = capsys.readouterr()

    assert ph.verify(updated_collaborator.password, "Passtest") == True
    assert (
        f"Le champ 'Mot de passe' du collaborateur n°{collaborator.id} a été mis à jour avec succès."
        in captured.out.strip()
    )


def test_department_update_successful(
    monkey_capture_message_collaborator,
    monkey_token_check_management,
    fake_collaborator_management,
    fake_department_management,
    capsys,
):
    """
    GIVEN a collaborator and a new department ID
    WHEN the update function is called to change the collaborator's department
    THEN the collaborator's department should be successfully updated, and a success message should be printed.
    """
    collaborator = fake_collaborator_management
    update(collaborator.id, 1, department=True)

    updated_collaborator = Collaborator.get(Collaborator.id == collaborator.id)

    captured = capsys.readouterr()

    assert updated_collaborator.department.id == 1
    assert (
        f"Le champ 'Département' du collaborateur n°{collaborator.id} a été mis à jour avec succès."
        in captured.out.strip()
    )


def test_department_update_unsuccessful(
    monkey_capture_message_collaborator,
    monkey_token_check_management,
    fake_collaborator_management,
    capsys,
):
    """
    GIVEN a collaborator and an invalid department ID
    WHEN the update function is called to change the collaborator's department
    THEN an Exit should be raised, and an error message should indicate an invalid department ID.
    """
    collaborator = fake_collaborator_management

    with pytest.raises(Exit):
        update(collaborator.id, "10", department=True)

    captured = capsys.readouterr()

    assert "Veuillez entrer un numéro de département valide." in captured.out.strip()


def test_collaborator_update_fails_without_attributes(
    monkey_capture_message_collaborator,
    monkey_token_check_management,
    fake_collaborator_management,
    capsys,
):
    """
    GIVEN a collaborator
    WHEN the update function is called without specifying any attribute
    THEN an Exit should be raised, and an error message should indicate that no attribute is selected for modification.
    """
    collaborator = fake_collaborator_management

    with pytest.raises(Exit):
        update(collaborator.id, "10")

    captured = capsys.readouterr()

    assert "Vous n'avez pas sélectionné d'attribut à modifier." in captured.out.strip()


def test_collaborator_update_fails_with_wrong_collaborator_id(
    monkey_capture_message_collaborator, monkey_token_check_management, capsys
):
    """
    GIVEN a non-existent collaborator ID and a new first name
    WHEN the update function is called to change a collaborator's first name
    THEN an error message should indicate that no collaborator is found with the provided ID.
    """
    fake_id = -100

    update(fake_id, "Gérard", first_name=True)

    captured = capsys.readouterr()

    assert f"Aucun collaborateur trouvé avec l'ID n°{fake_id}." in captured.out.strip()


def test_collaborator_update_not_authorized(
    monkey_capture_message_collaborator,
    monkey_token_check_correct_sales,
    fake_collaborator_management,
    capsys,
):
    """
    GIVEN a collaborator and incorrect authorization
    WHEN the update function is called to change an attribute of the collaborator
    THEN an Exit should be raised, and an error message should indicate restricted action.
    """
    collaborator = fake_collaborator_management

    with pytest.raises(Exit):
        update(collaborator.id, "Gérard", first_name=True)

    captured = capsys.readouterr()

    assert "Action restreinte." in captured.out.strip()


def test_collaborator_update_fails_without_authentication(
    monkey_capture_message_collaborator,
    monkey_token_check_false,
    fake_collaborator_management,
    capsys,
):
    """
    GIVEN a collaborator and no authentication
    WHEN the update function is called to change an attribute of the collaborator
    THEN an Exit should be raised, and an error message should indicate the need for authentication.
    """
    collaborator = fake_collaborator_management

    with pytest.raises(Exit):
        update(collaborator.id, "Gérard", first_name=True)

    captured = capsys.readouterr()

    assert "Veuillez vous authentifier et réessayer." in captured.out.strip()
