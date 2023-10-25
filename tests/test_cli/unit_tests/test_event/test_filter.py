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
    filter(s=True)

    captured = capsys.readouterr()
    
    print(captured)

    assert "À" in captured.out.strip()


def test_filter_support_with_management_collaborator_fails_with_null_queryset(
    monkey_token_check_management,
    capsys,
):
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
    filter(s=True)

    captured = capsys.readouterr()

    assert "Fake" in captured.out.strip()


def test_filter_support_with_support_collaborator_fails_with_null_queryset(
    monkey_token_check_support_gargamel,
    capsys,
):
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
    with pytest.raises(Exit):
        filter()

    captured = capsys.readouterr()

    assert "Veuillez vous authentifier et réessayer." in captured.out.strip()
