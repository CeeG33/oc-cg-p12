import pytest, os
from click.exceptions import Exit
from epicevents.cli.collaborator import login


def test_login_successful(
    monkey_dotenv, fake_collaborator_management, fake_department_management, capsys
):
    email = "test@management.fr"
    password = "testpass"

    login(email, password)

    captured = capsys.readouterr()

    assert captured.out.strip() == "Authentification réussie."


def test_login_with_wrong_email(monkey_dotenv, fake_collaborator_management, capsys):
    email = "test@wrong.fr"
    password = "testpass"

    with pytest.raises(Exit):
        login(email, password)

    captured = capsys.readouterr()

    assert captured.out.strip() == "Nom d'utilisateur ou mot de passe incorrect."


def test_login_with_wrong_password(monkey_dotenv, fake_collaborator_management, capsys):
    email = "test@company.fr"
    password = "wrong"

    with pytest.raises(Exit):
        login(email, password)

    captured = capsys.readouterr()

    assert captured.out.strip() == "Nom d'utilisateur ou mot de passe incorrect."
