import pytest, os
from click.exceptions import Exit
from epicevents.cli.collaborator import login


def test_login_successful(
    monkey_dotenv, fake_collaborator_management, fake_department_management, capsys
):
    """
    GIVEN a management collaborator and their correct email and password
    WHEN the login function is called with the correct email and password
    THEN it should authenticate the user successfully with a confirmation message.
    """
    email = "test@management.fr"
    password = "testpass"

    login(email, password)

    captured = capsys.readouterr()

    assert captured.out.strip() == "Authentification réussie."


def test_login_with_wrong_email(monkey_dotenv, fake_collaborator_management, capsys):
    """
    GIVEN a management collaborator and an incorrect email
    WHEN the login function is called with the wrong email and correct password
    THEN it should fail to authenticate the user and an error message should indicate that the email or password is incorrect.
    """
    email = "test@wrong.fr"
    password = "testpass"

    with pytest.raises(Exit):
        login(email, password)

    captured = capsys.readouterr()

    assert captured.out.strip() == "Nom d'utilisateur ou mot de passe incorrect."


def test_login_with_wrong_password(monkey_dotenv, fake_collaborator_management, capsys):
    """
    GIVEN a management collaborator and their correct email, but a wrong password
    WHEN the login function is called with the correct email and the wrong password
    THEN it should fail to authenticate the user and an error message should indicate that the email or password is incorrect.
    """
    email = "test@company.fr"
    password = "wrong"

    with pytest.raises(Exit):
        login(email, password)

    captured = capsys.readouterr()

    assert captured.out.strip() == "Nom d'utilisateur ou mot de passe incorrect."
