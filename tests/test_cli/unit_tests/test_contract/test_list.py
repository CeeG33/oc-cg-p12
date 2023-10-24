import pytest
from typer import Exit
from epicevents.cli.collaborator import _memorize_token
from epicevents.cli.contract import list
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError


def test_list_successful(monkey_token_check_management, fake_contract, capsys):
    list()

    captured = capsys.readouterr()

    assert "[ID]" in captured.out.strip()


def test_list_token_fails(monkey_token_check_false, fake_contract, capsys):
    with pytest.raises(Exit):
        list()

    captured = capsys.readouterr()

    assert "Veuillez vous authentifier et réessayer." in captured.out.strip()
