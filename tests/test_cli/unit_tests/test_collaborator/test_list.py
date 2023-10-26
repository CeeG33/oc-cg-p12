import pytest
from typer import Exit
from epicevents.data_access_layer.collaborator import Collaborator
from epicevents.cli.collaborator import list, _memorize_token, _verify_token
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError


def test_list_successful(
    monkey_token_check_management,
    fake_department_management,
    fake_collaborator_management,
    capsys,
):
    """
    GIVEN a management collaborator with a management department
    WHEN the list function is called
    THEN it should display a list of collaborators, and the output should contain "[ID]".
    """
    list()

    captured = capsys.readouterr()

    assert "[ID]" in captured.out.strip()


def test_list_not_allowed(monkey_token_check_correct_sales, capsys):
    """
    GIVEN a sales collaborator
    WHEN the list function is called
    THEN an Exit exception should be raised, and an error message should indicate a restricted action.
    """
    with pytest.raises(Exit):
        list()

    captured = capsys.readouterr()

    assert "Action restreinte." in captured.out.strip()


def test_list_fails_with_wrong_token(monkey_token_check_false, capsys):
    """
    GIVEN an unauthenticated state (wrong token)
    WHEN the list function is called
    THEN an Exit exception should be raised, and an error message should prompt the user to authenticate and try again.
    """
    with pytest.raises(Exit):
        list()

    captured = capsys.readouterr()

    assert "Veuillez vous authentifier et réessayer." in captured.out.strip()
