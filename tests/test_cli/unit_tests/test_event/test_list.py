import pytest
from typer import Exit
from epicevents.cli.event import list
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError


def test_list_successful(monkey_token_check_management, fake_event, capsys):
    list()

    captured = capsys.readouterr()

    assert "Tableau des évènements" in captured.out.strip()
    

def test_list_unsuccessful_with_null_database(monkey_token_check_support_gargamel, capsys):
    with pytest.raises(Exit):
        list()

    captured = capsys.readouterr()

    assert "La base de donnée ne contient aucun évènement." in captured.out.strip()


def test_list_token_fails(monkey_token_check_false, capsys):
    with pytest.raises(Exit):
        list()

    captured = capsys.readouterr()

    assert "Veuillez vous authentifier et réessayer." in captured.out.strip()
