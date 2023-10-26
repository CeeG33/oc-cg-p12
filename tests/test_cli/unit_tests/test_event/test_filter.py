import pytest
from typer import Exit
from epicevents.cli.event import filter
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError


def test_filter_support_with_management_collaborator_successful(
    monkey_token_check_management,
    fake_event,
    fake_event2,
    fake_event_no_support,
    fake_event_no_support_2,
    capsys,
):
    """
    GIVEN a management collaborator with the correct token and a dataset of events including some with support assigned
    WHEN the filter() function is called with the 's' filter to filter events with support assigned
    THEN the function should display events with support assigned
    """
    filter(s=True)

    captured = capsys.readouterr()

    assert "À" in captured.out.strip()


def test_filter_support_with_management_collaborator_fails_with_null_queryset(
    monkey_token_check_management,
    capsys,
):
    """
    GIVEN a management collaborator with the correct token and an empty dataset of events
    WHEN the filter() function is called with the 's' filter to filter events with support assigned
    THEN the function should raise an exit error, and an error message should indicate that all events have support assigned
    """
    with pytest.raises(Exit):
        filter(s=True)

    captured = capsys.readouterr()

    assert "Tous les évènements ont un assistant en charge !" in captured.out.strip()


def test_filter_support_with_support_collaborator_successful(
    monkey_token_check_support,
    fake_event,
    fake_event2,
    fake_event_no_support,
    fake_event_no_support_2,
    capsys,
):
    """
    GIVEN a support collaborator with the correct token and a dataset of events including some assigned to him
    WHEN the filter() function is called with the 's' filter to filter events with support assigned
    THEN the function should display events assigned to the support collaborator
    """
    filter(s=True)

    captured = capsys.readouterr()

    assert "Fake" in captured.out.strip()


def test_filter_support_with_support_collaborator_fails_with_null_queryset(
    monkey_token_check_support_gargamel,
    capsys,
):
    """
    GIVEN a support collaborator with the correct token and an empty dataset of events
    WHEN the filter() function is called with the 's' filter to filter events with support assigned
    THEN the function should raise an exit error, and an error message should indicate that the collaborator has no assigned events
    """
    with pytest.raises(Exit):
        filter(s=True)

    captured = capsys.readouterr()

    assert "Vous n'avez pas d'évènement affecté." in captured.out.strip()


def test_filter_fails_without_attribute(
    monkey_token_check_management,
    fake_event,
    fake_event2,
    fake_event_no_support,
    fake_event_no_support_2,
    capsys,
):
    """
    GIVEN a management collaborator with the correct token and a dataset of events
    WHEN the filter() function is called without specifying any filter attribute
    THEN the function should raise an exit error, and an error message should indicate that a filter attribute must be selected
    """

    with pytest.raises(Exit):
        filter()

    captured = capsys.readouterr()

    assert "Vous n'avez pas sélectionné de filtre à appliquer." in captured.out.strip()


def test_filter_not_authorized(
    monkey_token_check_correct_sales,
    fake_event,
    fake_event2,
    fake_event_no_support,
    fake_event_no_support_2,
    capsys,
):
    """
    GIVEN a sales collaborator with the correct token and a dataset of events
    WHEN the filter() function is called without specifying any filter attribute
    THEN the function should raise an exit error, and an error message should indicate that the action is restricted
    """
    with pytest.raises(Exit):
        filter()

    captured = capsys.readouterr()

    assert "Action restreinte." in captured.out.strip()


def test_filter_fails_without_authentication(
    monkey_token_check_false,
    fake_event,
    fake_event2,
    fake_event_no_support,
    fake_event_no_support_2,
    capsys,
):
    """
    GIVEN an unauthenticated collaborator and a dataset of events
    WHEN the filter() function is called without specifying any filter attribute
    THEN the function should raise an exit error, and an error message should indicate that authentication is required
    """
    with pytest.raises(Exit):
        filter()

    captured = capsys.readouterr()

    assert "Veuillez vous authentifier et réessayer." in captured.out.strip()
