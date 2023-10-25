import pytest
from typer import Exit
from epicevents.cli.client import list
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError


def test_list_successful(monkey_token_check_management, fake_client, capsys):
    list()

    captured = capsys.readouterr()
    
    print(captured)

    assert "Tableau des clients" in captured.out.strip()
    
def test_list_fails_with_empty_database(monkey_token_check_management, capsys):
    with pytest.raises(Exit):
        list()
    
    captured = capsys.readouterr()

    assert "La base de donnée ne contient aucun client." in captured.out.strip()

def test_list_token_fails(monkey_token_check_false, fake_client, capsys):
    with pytest.raises(Exit):
        list()
    
    captured = capsys.readouterr()

    assert "Veuillez vous authentifier et réessayer." in captured.out.strip()

