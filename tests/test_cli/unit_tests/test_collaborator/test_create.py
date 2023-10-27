import pytest
from typer import Exit
from epicevents.cli.collaborator import create


def test_creation_successful(
    monkey_capture_message_collaborator,
    monkey_token_check_management,
    fake_department_management,
    capsys,
):
    """
    GIVEN a management collaborator with the correct token and an existing management department,
    WHEN the create() function is called to create a new collaborator,
    THEN a collaborator should be created successfully, and a success message should be printed.
    """
    create(
        first_name="Collab",
        name="Test",
        email="collab@test.fr",
        password="Passtest",
        department=1,
    )

    captured = capsys.readouterr()

    assert "a été créé avec succès." in captured.out.strip()


def test_creation_fails_with_wrong_department(
    monkey_capture_message_collaborator, monkey_token_check_management, capsys
):
    """
    GIVEN a management collaborator with the correct token,
    WHEN the create() function is called to create a new collaborator with an invalid department ID,
    THEN an Exit exception should be raised, and an error message indicating an invalid department should be printed.
    """
    with pytest.raises(Exit):
        create(
            first_name="Collab",
            name="Test",
            email="collab@test.fr",
            password="Passtest",
            department=-100,
        )

    captured = capsys.readouterr()

    assert "Aucun département trouvé" in captured.out.strip()


def test_creation_not_allowed(monkey_token_check_fake_sales, capsys):
    """
    GIVEN a fake sales collaborator with the correct token,
    WHEN the create() function is called to create a new collaborator,
    THEN an Exit exception should be raised, and an error message should indicate a restricted action.
    """
    with pytest.raises(Exit):
        create(
            first_name="Collab",
            name="Test",
            email="collab@test.fr",
            password="Passtest",
            department=1,
        )

    captured = capsys.readouterr()

    assert "Action restreinte." in captured.out.strip()


def test_creation_token_fails(monkey_token_check_false, capsys):
    """
    GIVEN an unauthenticated user,
    WHEN the create() function is called to create a new collaborator,
    THEN an Exit exception should be raised, and an error message should prompt the user to authenticate and try again.
    """
    with pytest.raises(Exit):
        create(
            first_name="Collab",
            name="Test",
            email="collabo@test.fr",
            password="Passtest",
            department=1,
        )

    captured = capsys.readouterr()

    assert "Veuillez vous authentifier et réessayer." in captured.out.strip()
