import pytest
from typer import Exit
from epicevents.cli.event import list


def test_list_successful(monkey_token_check_management, fake_event, capsys):
    """
    GIVEN a collaborator with management privileges and a dataset of events
    WHEN the list() function is called
    THEN the function should display a table of events
    """
    list()

    captured = capsys.readouterr()

    assert "Tableau des évènements" in captured.out.strip()


def test_list_unsuccessful_with_null_database(
    monkey_token_check_support_gargamel, capsys
):
    """
    GIVEN a collaborator with support privileges and an empty dataset of events
    WHEN the list() function is called
    THEN the function should raise an exit error, and an error message should indicate that the database contains no events
    """
    with pytest.raises(Exit):
        list()

    captured = capsys.readouterr()

    assert "La base de donnée ne contient aucun évènement." in captured.out.strip()


def test_list_token_fails(monkey_token_check_false, capsys):
    """
    GIVEN an unauthenticated collaborator and a dataset of events
    WHEN the list() function is called
    THEN the function should raise an exit error, and an error message should indicate that authentication is required
    """
    with pytest.raises(Exit):
        list()

    captured = capsys.readouterr()

    assert "Veuillez vous authentifier et réessayer." in captured.out.strip()
