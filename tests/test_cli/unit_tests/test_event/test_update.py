import pytest
from datetime import datetime
from typer import Exit
from peewee import DoesNotExist
from epicevents.data_access_layer.event import Event
from epicevents.cli.event import update
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError


def test_contract_update_successful(
    monkey_token_check_management, fake_event, fake_contract, capsys
):
    update(fake_event.id, fake_contract.id, contract=True)

    updated_event = Event.get(Event.id == fake_event.id)

    captured = capsys.readouterr()

    assert updated_event.contract.id == fake_contract.id
    assert updated_event.contract.total_sum == fake_contract.total_sum
    assert (
        f"Le champ 'Contrat' de l'évènement n°{fake_event.id} a été mis à jour avec succès."
        in captured.out.strip()
    )


def test_contract_update_fails_with_wrong_id(
    monkey_token_check_management, fake_event, capsys
):
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
    update(fake_event.id, fake_collaborator_support2.id, support=True)

    updated_event = Event.get(Event.id == fake_event.id)

    captured = capsys.readouterr()

    assert updated_event.support.id == fake_collaborator_support2.id
    assert updated_event.support.first_name == fake_collaborator_support2.first_name
    assert (
        f"Le champ 'Assistant en charge' de l'évènement n°{fake_event.id} a été mis à jour avec succès."
        in captured.out.strip()
    )


def test_support_update_fails_with_wrong_id(
    monkey_token_check_management, fake_event, capsys
):
    with pytest.raises(Exit):
        update(fake_event.id, -50, support=True)

    captured = capsys.readouterr()

    assert (
        "Veuillez entrer un numéro de collaborateur valide et faisant partie du département Support."
        in captured.out.strip()
    )


def test_support_update_fails_with_not_support_collaborator(
    monkey_token_check_management,
    fake_event,
    fake_department_management,
    fake_department_sales,
    fake_collaborator_sales,
    capsys,
):
    with pytest.raises(Exit):
        update(fake_event.id, fake_collaborator_sales.id, support=True)

    captured = capsys.readouterr()

    assert (
        "Veuillez entrer un numéro de collaborateur valide et faisant partie du département Support."
        in captured.out.strip()
    )


def test_start_date_update_successful(
    monkey_token_check_management, fake_event, capsys
):
    new_start_date = "2024-01-25 15:00"
    update(fake_event.id, new_start_date, start_date=True)

    updated_event = Event.get(Event.id == fake_event.id)

    captured = capsys.readouterr()

    assert updated_event.start_date == new_start_date
    assert (
        f"Le champ 'Date de début' de l'évènement n°{fake_event.id} a été mis à jour avec succès."
        in captured.out.strip()
    )
    assert (
        "Veuillez également penser à modifier la date de fin." in captured.out.strip()
    )


def test_end_date_update_successful(monkey_token_check_management, fake_event, capsys):
    new_end_date = "2024-01-25 20:00"
    update(fake_event.id, new_end_date, end_date=True)

    updated_event = Event.get(Event.id == fake_event.id)

    captured = capsys.readouterr()

    assert updated_event.end_date == new_end_date
    assert (
        f"Le champ 'Date de fin' de l'évènement n°{fake_event.id} a été mis à jour avec succès."
        in captured.out.strip()
    )
    assert (
        "Avez-vous également pensé à modifier la date de début ?"
        in captured.out.strip()
    )


def test_location_update_successful(monkey_token_check_management, fake_event, capsys):
    new_location = "54, rue des Castors - 75005 PARIS"
    update(fake_event.id, new_location, location=True)

    updated_event = Event.get(Event.id == fake_event.id)

    captured = capsys.readouterr()

    assert updated_event.location == new_location
    assert (
        f"Le champ 'Localisation' de l'évènement n°{fake_event.id} a été mis à jour avec succès."
        in captured.out.strip()
    )


def test_attendees_update_successful(monkey_token_check_management, fake_event, capsys):
    new_attendees = 15
    update(fake_event.id, new_attendees, attendees=True)

    updated_event = Event.get(Event.id == fake_event.id)

    captured = capsys.readouterr()

    assert updated_event.attendees == new_attendees
    assert (
        f"Le champ 'Nombre de participants' de l'évènement n°{fake_event.id} a été mis à jour avec succès."
        in captured.out.strip()
    )


def test_notes_update_successful(monkey_token_check_management, fake_event, capsys):
    new_notes = "Test notes"
    update(fake_event.id, new_notes, notes=True)

    updated_event = Event.get(Event.id == fake_event.id)

    captured = capsys.readouterr()

    assert updated_event.notes == new_notes
    assert (
        f"Le champ 'Notes' de l'évènement n°{fake_event.id} a été mis à jour avec succès."
        in captured.out.strip()
    )


def test_update_fails_without_attribute(
    monkey_token_check_management, fake_event, capsys
):
    with pytest.raises(Exit):
        update(fake_event.id, "Test")

    captured = capsys.readouterr()

    assert "Vous n'avez pas sélectionné d'attribut à modifier." in captured.out.strip()


def test_update_not_authorized_for_sales_collaborator(
    monkey_token_check_correct_sales, fake_event, capsys
):
    with pytest.raises(Exit):
        update(fake_event.id, "Test notes", notes=True)

    captured = capsys.readouterr()

    assert "Action restreinte." in captured.out.strip()


def test_update_not_authorized_for_support_collaborator(
    monkey_token_check_support_gargamel, fake_event, capsys
):
    with pytest.raises(Exit):
        update(fake_event.id, "Test notes", notes=True)

    captured = capsys.readouterr()

    assert "Action restreinte." in captured.out.strip()


def test_update_fails_without_authentication(
    monkey_token_check_false, fake_event, capsys
):
    with pytest.raises(Exit):
        update(fake_event.id, "Test notes", notes=True)

    captured = capsys.readouterr()

    assert "Veuillez vous authentifier et réessayer." in captured.out.strip()
