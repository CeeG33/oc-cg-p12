import pytest
from typer import Exit
from epicevents.data_access_layer.event import Event
from epicevents.cli.event import update


def test_contract_update_successful(
    monkey_token_check_management, fake_event, fake_contract, capsys
):
    """
    GIVEN a collaborator with management privileges, an event, and a contract
    WHEN the update() function is called to update the contract of the event
    THEN the function should update the event's contract to the provided contract, display a success message, and update related attributes
    """
    update(fake_event.id, fake_contract.id, contract=True)

    updated_event = Event.get(Event.id == fake_event.id)

    captured = capsys.readouterr()

    assert updated_event.contract.id == fake_contract.id
    assert updated_event.contract.total_sum == fake_contract.total_sum
    assert "Contrat" in captured.out.strip()


def test_contract_update_fails_with_wrong_id(
    monkey_token_check_management, fake_event, capsys
):
    """
    GIVEN a collaborator with management privileges and an event
    WHEN the update() function is called with an invalid contract ID to update the event's contract
    THEN the function should raise an exit error with an error message indicating that a valid contract ID is required
    """
    with pytest.raises(Exit):
        update(fake_event.id, -50, contract=True)

    captured = capsys.readouterr()

    assert "Veuillez entrer un numéro de contrat valide." in captured.out.strip()


def test_support_update_successful(
    monkey_token_check_management,
    fake_department_management,
    fake_department_sales,
    fake_department_support,
    fake_event,
    fake_collaborator_support2,
    capsys,
):
    """
    GIVEN a collaborator with management privileges, departments, an event, and a collaborator to be assigned as support
    WHEN the update() function is called to update the support collaborator of the event
    THEN the function should update the event's support collaborator to the provided collaborator, display a success message, and update related attributes
    """
    update(fake_event.id, fake_collaborator_support2.id, support=True)

    updated_event = Event.get(Event.id == fake_event.id)

    captured = capsys.readouterr()

    assert updated_event.support.id == fake_collaborator_support2.id
    assert updated_event.support.first_name == fake_collaborator_support2.first_name
    assert "Assistant en charge" in captured.out.strip()


def test_support_update_fails_with_wrong_id(
    monkey_token_check_management, fake_event, capsys
):
    """
    GIVEN a collaborator with management privileges and an event
    WHEN the update() function is called with an invalid collaborator ID to update the event's support collaborator
    THEN the function should raise an exit error with an error message indicating that a valid collaborator ID is required
    """
    with pytest.raises(Exit):
        update(fake_event.id, -50, support=True)

    captured = capsys.readouterr()

    assert "valide" in captured.out.strip()


def test_support_update_fails_with_not_support_collaborator(
    monkey_token_check_management,
    fake_event,
    fake_department_management,
    fake_department_sales,
    fake_collaborator_sales,
    capsys,
):
    """
    GIVEN a collaborator with management privileges, departments, an event, and a sales collaborator to be assigned as support
    WHEN the update() function is called to update the support collaborator of the event
    THEN the function should raise an exit error with an error message indicating that a valid support collaborator is required
    """
    with pytest.raises(Exit):
        update(fake_event.id, fake_collaborator_sales.id, support=True)

    captured = capsys.readouterr()

    assert "valide" in captured.out.strip()


def test_start_date_update_successful(
    monkey_token_check_management, fake_event, capsys
):
    """
    GIVEN a collaborator with management privileges and an event
    WHEN the update() function is called to update the start date of the event
    THEN the function should update the event's start date, display a success message, and provide a reminder about updating the end date as well
    """
    new_start_date = "2024-01-25 15:00"
    update(fake_event.id, new_start_date, start_date=True)

    updated_event = Event.get(Event.id == fake_event.id)

    captured = capsys.readouterr()

    assert updated_event.start_date == new_start_date
    assert f"Date de début" in captured.out.strip()
    assert (
        "Veuillez également penser à modifier la date de fin." in captured.out.strip()
    )


def test_end_date_update_successful(monkey_token_check_management, fake_event, capsys):
    """
    GIVEN a collaborator with management privileges and an event
    WHEN the update() function is called to update the end date of the event
    THEN the function should update the event's end date, display a success message, and provide a reminder about updating the start date as well
    """
    new_end_date = "2024-01-25 20:00"
    update(fake_event.id, new_end_date, end_date=True)

    updated_event = Event.get(Event.id == fake_event.id)

    captured = capsys.readouterr()

    assert updated_event.end_date == new_end_date
    assert f"Date de fin" in captured.out.strip()
    assert (
        "Avez-vous également pensé à modifier la date de début ?"
        in captured.out.strip()
    )


def test_location_update_successful(monkey_token_check_management, fake_event, capsys):
    """
    GIVEN a collaborator with management privileges and an event
    WHEN the update() function is called to update the location of the event
    THEN the function should update the event's location, display a success message, and update related attributes
    """
    new_location = "54, rue des Castors - 75005 PARIS"
    update(fake_event.id, new_location, location=True)

    updated_event = Event.get(Event.id == fake_event.id)

    captured = capsys.readouterr()

    assert updated_event.location == new_location
    assert f"Localisation" in captured.out.strip()


def test_attendees_update_successful(monkey_token_check_management, fake_event, capsys):
    """
    GIVEN a collaborator with management privileges and an event
    WHEN the update() function is called to update the number of attendees of the event
    THEN the function should update the event's number of attendees, display a success message, and update related attributes
    """
    new_attendees = 15
    update(fake_event.id, new_attendees, attendees=True)

    updated_event = Event.get(Event.id == fake_event.id)

    captured = capsys.readouterr()

    assert updated_event.attendees == new_attendees
    assert f"Nombre de participants" in captured.out.strip()


def test_notes_update_successful(monkey_token_check_management, fake_event, capsys):
    """
    GIVEN a collaborator with management privileges and an event
    WHEN the update() function is called to update the notes of the event
    THEN the function should update the event's notes, display a success message, and update related attributes
    """
    new_notes = "Test notes"
    update(fake_event.id, new_notes, notes=True)

    updated_event = Event.get(Event.id == fake_event.id)

    captured = capsys.readouterr()

    assert updated_event.notes == new_notes
    assert f"Notes" in captured.out.strip()


def test_update_fails_without_attribute(
    monkey_token_check_management, fake_event, capsys
):
    """
    GIVEN a collaborator with management privileges and an event
    WHEN the update() function is called without specifying an attribute to update
    THEN the function should raise an exit error with an error message indicating that an attribute to modify must be selected
    """
    with pytest.raises(Exit):
        update(fake_event.id, "Test")

    captured = capsys.readouterr()

    assert "Vous n'avez pas sélectionné d'attribut à modifier." in captured.out.strip()


def test_update_not_authorized_for_sales_collaborator(
    monkey_token_check_correct_sales, fake_event, capsys
):
    """
    GIVEN a sales collaborator and an event
    WHEN the update() function is called to update an attribute of the event
    THEN the function should raise an exit error with an error message indicating that the action is restricted
    """
    with pytest.raises(Exit):
        update(fake_event.id, "Test notes", notes=True)

    captured = capsys.readouterr()

    assert "Action restreinte." in captured.out.strip()


def test_update_not_authorized_for_support_collaborator(
    monkey_token_check_support_gargamel, fake_event, capsys
):
    """
    GIVEN a support collaborator and an event
    WHEN the update() function is called to update an attribute of the event
    THEN the function should raise an exit error with an error message indicating that the action is restricted
    """
    with pytest.raises(Exit):
        update(fake_event.id, "Test notes", notes=True)

    captured = capsys.readouterr()

    assert "Action restreinte." in captured.out.strip()


def test_update_fails_without_authentication(
    monkey_token_check_false, fake_event, capsys
):
    """
    GIVEN an unauthenticated user and an event
    WHEN the update() function is called to update an attribute of the event
    THEN the function should raise an exit error with an error message indicating that authentication is required
    """
    with pytest.raises(Exit):
        update(fake_event.id, "Test notes", notes=True)

    captured = capsys.readouterr()

    assert "Veuillez vous authentifier et réessayer." in captured.out.strip()
