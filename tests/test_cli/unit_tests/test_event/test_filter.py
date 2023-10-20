import pytest
from typer import Exit
from epicevents.cli.event import filter
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError


def test_filter_support_with_management_collaborator_successful(monkey_token_check_management, fake_event, fake_event2, fake_event_no_support, fake_event_no_support_2, capsys):
    filter(s=True)

    captured = capsys.readouterr()
    
    assert "[Assistant en charge] : À définir" in captured.out.strip()
    assert "3, rue de Paris - 75000 PARIS" in captured.out.strip()
    assert "23, av des Champs Elysées - 75008 PARIS" in captured.out.strip()
    
def test_filter_support_with_support_collaborator_successful(monkey_token_check_support, fake_event, fake_event2, fake_event_no_support, fake_event_no_support_2, capsys):
    filter(s=True)

    captured = capsys.readouterr()
    
    assert "[Assistant en charge] : Fake Collaborator" in captured.out.strip()
    assert "55, rue des Acacias - 77093 VILLEFANTOME" in captured.out.strip()
    assert "MARSEILLE" in captured.out.strip()
    
def test_filter_fails_without_attribute(monkey_token_check_management, fake_event, fake_event2, fake_event_no_support, fake_event_no_support_2, capsys):
    with pytest.raises(Exit):
        filter()

    captured = capsys.readouterr()
    
    assert "Vous n'avez pas sélectionné de filtre à appliquer." in captured.out.strip()
    
def test_filter_not_authorized(monkey_token_check_correct_sales, fake_event, fake_event2, fake_event_no_support, fake_event_no_support_2, capsys):
    with pytest.raises(Exit):
        filter()

    captured = capsys.readouterr()
    
    assert "Action restreinte." in captured.out.strip()
    
def test_filter_fails_without_authentication(monkey_token_check_false, fake_event, fake_event2, fake_event_no_support, fake_event_no_support_2, capsys):
    with pytest.raises(Exit):
        filter()

    captured = capsys.readouterr()
    
    assert "Veuillez vous authentifier et réessayer." in captured.out.strip()


