import pytest
from typer import Exit
from epicevents.data_access_layer.event import Event
from epicevents.cli.event import create


def test_creation_successful(monkey_token_check_correct_sales, fake_contract, capsys):
    """
    GIVEN a sales collaborator with the correct token, an existing contract, and valid event data
    WHEN the create() function is called to create an event
    THEN the event should be created with the given data, and a success message should be printed
    """
    contract = fake_contract.id
    start_date = "2024-05-20 14:00"
    end_date = "2024-05-20 22:00"
    location = "102, rue des Chiens - 92000 NANTERRE"
    attendees = 6

    create(
        contract=contract,
        start_date=start_date,
        end_date=end_date,
        location=location,
        attendees=attendees,
    )

    created_event = Event.get(Event.location == location)

    captured = capsys.readouterr()

    assert created_event.contract.id == contract
    assert created_event.start_date == start_date
    assert created_event.end_date == end_date
    assert created_event.location == location
    assert created_event.attendees == attendees
    assert "L'évènement a été créé avec succès." in captured.out.strip()

    created_event.delete_instance()


def test_creation_with_optional_arguments_successful(
    monkey_token_check_correct_sales, fake_contract, fake_collaborator_support, capsys
):
    """
    GIVEN a sales collaborator with the correct token, an existing contract, and valid event data including optional arguments
    WHEN the create() function is called to create an event
    THEN the event should be created with the given data, including optional arguments, and a success message should be printed
    """
    contract = fake_contract.id
    start_date = "2024-05-20 14:00"
    end_date = "2024-05-20 22:00"
    location = "223, rue des Chèvres - 92000 NANTERRE"
    attendees = 6
    notes = "Ceci est un test"
    support = fake_collaborator_support.id

    create(
        contract=contract,
        start_date=start_date,
        end_date=end_date,
        location=location,
        attendees=attendees,
        notes=notes,
        support=support,
    )

    created_event = Event.get(Event.location == location)

    captured = capsys.readouterr()

    assert created_event.contract.id == contract
    assert created_event.start_date == start_date
    assert created_event.end_date == end_date
    assert created_event.location == location
    assert created_event.attendees == attendees
    assert created_event.notes == notes
    assert created_event.support.id == support
    assert "L'évènement a été créé avec succès." in captured.out.strip()

    created_event.delete_instance()


def test_contract_not_found(monkey_token_check_correct_sales, fake_contract, capsys):
    """
    GIVEN a sales collaborator with the correct token and non-existing contract ID, and valid event data
    WHEN the create() function is called to create an event
    THEN the function should raise an exit error, and an error message should indicate that a valid contract ID is required
    """
    contract = -100
    start_date = "2024-05-20 14:00"
    end_date = "2024-05-20 22:00"
    location = "98, rue des Chats - 92000 NANTERRE"
    attendees = 6

    with pytest.raises(Exit):
        create(
            contract=contract,
            start_date=start_date,
            end_date=end_date,
            location=location,
            attendees=attendees,
        )

    created_event = Event.get_or_none(Event.location == location)

    captured = capsys.readouterr()

    assert "Veuillez entrer un numéro de contrat valide." in captured.out.strip()
    assert created_event == None


def test_support_not_found(monkey_token_check_correct_sales, fake_contract, capsys):
    """
    GIVEN a sales collaborator with the correct token, an existing contract, and valid event data including an invalid support ID
    WHEN the create() function is called to create an event
    THEN the function should raise an exit error, and an error message should indicate that a valid support ID is required
    """
    contract = fake_contract.id
    start_date = "2024-05-20 14:00"
    end_date = "2024-05-20 22:00"
    location = "98, rue des Chats - 92000 NANTERRE"
    attendees = 6
    support = -100

    with pytest.raises(Exit):
        create(
            contract=contract,
            start_date=start_date,
            end_date=end_date,
            location=location,
            attendees=attendees,
            support=support,
        )

    created_event = Event.get_or_none(Event.location == location)

    captured = capsys.readouterr()

    assert "Veuillez entrer un numéro de support valide." in captured.out.strip()
    assert created_event == None


def test_creation_fails_with_wrong_salesman(
    monkey_token_check_correct_sales_plankton, fake_contract, capsys
):
    """
    GIVEN a sales collaborator with the incorrect sales token, an existing contract, and valid event data
    WHEN the create() function is called to create an event
    THEN the function should raise an exit error, and an error message should indicate that the action is restricted
    """
    contract = fake_contract.id
    start_date = "2024-05-20 14:00"
    end_date = "2024-05-20 22:00"
    location = "98, rue des Chats - 92000 NANTERRE"
    attendees = 6

    with pytest.raises(Exit):
        create(
            contract=contract,
            start_date=start_date,
            end_date=end_date,
            location=location,
            attendees=attendees,
        )
    created_event = Event.get_or_none(Event.location == location)

    captured = capsys.readouterr()

    assert "affecté" in captured.out.strip()
    assert created_event == None


def test_creation_fails_with_unsigned_contract(
    monkey_token_check_correct_sales, fake_contract_unsigned, capsys
):
    """
    GIVEN a sales collaborator with the correct token, an existing unsigned contract, and valid event data
    WHEN the create() function is called to create an event
    THEN the function should raise an exit error, and an error message should indicate that events cannot be created for unsigned contracts
    """
    contract = fake_contract_unsigned.id
    start_date = "2024-05-20 14:00"
    end_date = "2024-05-20 22:00"
    location = "98, rue des Chats - 92000 NANTERRE"
    attendees = 6

    with pytest.raises(Exit):
        create(
            contract=contract,
            start_date=start_date,
            end_date=end_date,
            location=location,
            attendees=attendees,
        )
    created_event = Event.get_or_none(Event.location == location)

    captured = capsys.readouterr()

    assert (
        "Vous ne pouvez pas créer d'évènement pour un contrat qui n'est pas signé."
        in captured.out.strip()
    )
    assert created_event == None


def test_creation_not_authorized(monkey_token_check_management, fake_contract, capsys):
    """
    GIVEN a management collaborator with the correct token, an existing contract, and valid event data
    WHEN the create() function is called to create an event
    THEN the function should raise an exit error, and an error message should indicate that the action is restricted
    """
    contract = fake_contract.id
    start_date = "2024-05-20 14:00"
    end_date = "2024-05-20 22:00"
    location = "98, rue des Chats - 92000 NANTERRE"
    attendees = 6

    with pytest.raises(Exit):
        create(
            contract=contract,
            start_date=start_date,
            end_date=end_date,
            location=location,
            attendees=attendees,
        )

    created_event = Event.get_or_none(Event.location == location)

    captured = capsys.readouterr()

    assert "Action restreinte." in captured.out.strip()
    assert created_event == None


def test_creation_fails_if_not_authenticated(
    monkey_token_check_false, fake_contract, capsys
):
    """
    GIVEN an unauthenticated collaborator, an existing contract, and valid event data
    WHEN the create() function is called to create an event
    THEN the function should raise an exit error, and an error message should indicate that authentication is required
    """
    contract = fake_contract.id
    start_date = "2024-05-20 14:00"
    end_date = "2024-05-20 22:00"
    location = "98, rue des Chats - 92000 NANTERRE"
    attendees = 6

    with pytest.raises(Exit):
        create(
            contract=contract,
            start_date=start_date,
            end_date=end_date,
            location=location,
            attendees=attendees,
        )

    created_event = Event.get_or_none(Event.location == location)

    captured = capsys.readouterr()

    assert "Veuillez vous authentifier et réessayer." in captured.out.strip()
    assert created_event == None
