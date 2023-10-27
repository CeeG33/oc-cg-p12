import pytest
from typer import Exit
from argon2 import PasswordHasher
from epicevents.data_access_layer.collaborator import Collaborator
from epicevents.cli.collaborator import delete


ph = PasswordHasher()


def test_collaborator_delete_successful(
    monkey_capture_message_collaborator,
    monkey_token_check_management,
    fake_collaborator_management,
    capsys,
):
    """
    GIVEN a management collaborator with the correct token and an existing management collaborator,
    WHEN the delete() function is called to delete the collaborator,
    THEN the collaborator should be deleted successfully, and a success message should be printed.
    """
    collaborator = fake_collaborator_management
    delete(collaborator.id)

    updated_collaborator = Collaborator.get_or_none(Collaborator.id == collaborator.id)

    captured = capsys.readouterr()

    assert updated_collaborator == None
    assert (
        f"Le collaborateur n°{collaborator.id} a été supprimé avec succès."
        in captured.out.strip()
    )


def test_collaborator_deletion_fails_with_wrong_collaborator_id(
    monkey_token_check_management, capsys
):
    """
    GIVEN a management collaborator with the correct token,
    WHEN the delete() function is called to delete a collaborator with an invalid ID,
    THEN an Exit exception should be raised, and an error message indicating that no collaborator was found with the given ID should be printed.
    """
    fake_id = -100

    delete(fake_id)

    captured = capsys.readouterr()

    assert f"Aucun collaborateur trouvé avec l'ID n°{fake_id}." in captured.out.strip()


def test_collaborator_deletion_not_authorized(
    monkey_token_check_correct_sales, fake_collaborator_management, capsys
):
    """
    GIVEN a sales collaborator with the correct token and an existing management collaborator,
    WHEN the delete() function is called to delete the collaborator,
    THEN an Exit exception should be raised, and an error message should indicate a restricted action.
    """
    collaborator = fake_collaborator_management

    with pytest.raises(Exit):
        delete(collaborator.id)

    captured = capsys.readouterr()

    assert "Action restreinte." in captured.out.strip()


def test_collaborator_deletion_fails_without_authentication(
    monkey_token_check_false, fake_collaborator_management, capsys
):
    """
    GIVEN an unauthenticated user and an existing management collaborator,
    WHEN the delete() function is called to delete the collaborator,
    THEN an Exit exception should be raised, and an error message should prompt the user to authenticate and try again.
    """
    collaborator = fake_collaborator_management

    with pytest.raises(Exit):
        delete(collaborator.id)

    captured = capsys.readouterr()

    assert "Veuillez vous authentifier et réessayer." in captured.out.strip()
