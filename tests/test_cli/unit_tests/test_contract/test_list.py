import pytest
from typer import Exit
from epicevents.cli.contract import list


def test_list_successful(monkey_token_check_management, fake_contract, capsys):
    """
    GIVEN a collaborator with the correct management token and a set of contracts
    WHEN the list() function is called to list contracts
    THEN the function should display the "Tableau des contrats" message indicating successful listing
    """
    list()

    captured = capsys.readouterr()

    assert "Tableau des contrats" in captured.out.strip()


def test_list_fails_with_empty_database(monkey_token_check_management, capsys):
    """
    GIVEN a collaborator with the correct management token and an empty set of contracts
    WHEN the list() function is called to list contracts
    THEN the function should raise an exit error, and an error message should indicate that the database contains no contracts
    """
    with pytest.raises(Exit):
        list()

    captured = capsys.readouterr()

    assert "La base de donnée ne contient aucun contrat." in captured.out.strip()


def test_list_token_fails(monkey_token_check_false, fake_contract, capsys):
    """
    GIVEN a collaborator with an incorrect token and a set of contracts
    WHEN the list() function is called to list contracts
    THEN the function should raise an exit error, and an error message should indicate that authentication is required
    """
    with pytest.raises(Exit):
        list()

    captured = capsys.readouterr()

    assert "Veuillez vous authentifier et réessayer." in captured.out.strip()
