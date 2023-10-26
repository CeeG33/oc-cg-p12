import pytest
from datetime import datetime
from epicevents.cli import event
from epicevents.data_access_layer.event import Event


def test_event_create_and_read_successful(
    monkey_token_check_correct_sales, fake_contract, capsys
):
    """
    Given a valid sales collaborator token,
    When an event is created with specific details,
    Then the event should be created and have the expected number of attendees.

    When listing events,
    Then the "Tableau des évènements" should appear in the output.
    """
    event.create(
        contract=fake_contract.id,
        start_date="2023-11-25 14:00",
        end_date="2023-11-25 22:00",
        location="36, quai des Orfèvres - 75001 PARIS",
        attendees=8,
    )

    created_event = Event.get(Event.location == "36, quai des Orfèvres - 75001 PARIS")

    assert created_event.attendees == 8

    event.list()

    captured = capsys.readouterr()

    assert "Tableau des évènements" in captured.out.strip()

    created_event.delete_instance()
