import pytest
from typer import Exit
from epicevents.cli.client import list


def test_list_successful(monkey_token_check_management, fake_client, capsys):
    """
    GIVEN a user with management access and existing clients in the database
    WHEN the list() function is called
    THEN it should print a table of clients with their information
    """
    list()

    captured = capsys.readouterr()

    print(captured)

    assert "Tableau des clients" in captured.out.strip()


def test_list_fails_with_empty_database(monkey_token_check_management, capsys):
    """
    GIVEN a user with management access but an empty client database
    WHEN the list() function is called
    THEN it should raise an Exit exception, and an error message should indicate that the database contains no clients
    """
    with pytest.raises(Exit):
        list()

    captured = capsys.readouterr()

    assert "La base de donnée ne contient aucun client." in captured.out.strip()


def test_list_token_fails(monkey_token_check_false, fake_client, capsys):
    """
    GIVEN a user with an invalid token and existing clients in the database
    WHEN the list() function is called
    THEN it should raise an Exit exception, and an error message should prompt the user to authenticate and try again
    """
    with pytest.raises(Exit):
        list()

    captured = capsys.readouterr()

    assert "Veuillez vous authentifier et réessayer." in captured.out.strip()
