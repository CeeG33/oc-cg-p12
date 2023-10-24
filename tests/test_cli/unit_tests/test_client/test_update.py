import pytest
from datetime import datetime
from typer import Exit
from peewee import DoesNotExist
from epicevents.data_access_layer.client import Client
from epicevents.cli.client import update
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError


def test_company_update(
    monkey_token_check_correct_sales, fake_client, fake_company2, capsys
):
    company = fake_company2.id
    update(fake_client.id, company, company=True)

    updated_client = Client.get(Client.id == fake_client.id)

    captured = capsys.readouterr()

    assert updated_client.company.id == company
    assert (
        f"Le champ 'Entreprise' du client n°{fake_client.id} a été mis à jour avec succès."
        in captured.out.strip()
    )


def test_company_not_found(monkey_token_check_correct_sales, fake_client, capsys):
    company = -100

    with pytest.raises(Exit):
        update(fake_client.id, company, company=True)

    updated_client = Client.get(Client.id == fake_client.id)

    captured = capsys.readouterr()

    assert updated_client.company.id == fake_client.company.id
    assert "Veuillez entrer un numéro d'entreprise valide." in captured.out.strip()


def test_first_name_update(monkey_token_check_correct_sales, fake_client, capsys):
    first_name = "Gégé"
    update(fake_client.id, first_name, first_name=True)

    updated_client = Client.get(Client.id == fake_client.id)

    captured = capsys.readouterr()

    assert updated_client.first_name == first_name
    assert (
        f"Le champ 'Prénom' du client n°{fake_client.id} a été mis à jour avec succès."
        in captured.out.strip()
    )


def test_name_update(monkey_token_check_correct_sales, fake_client, capsys):
    name = "Lanbrouille"
    update(fake_client.id, name, name=True)

    updated_client = Client.get(Client.id == fake_client.id)

    captured = capsys.readouterr()

    assert updated_client.name == name
    assert (
        f"Le champ 'Nom' du client n°{fake_client.id} a été mis à jour avec succès."
        in captured.out.strip()
    )


def test_email_update(monkey_token_check_correct_sales, fake_client, capsys):
    email = "gege.lanbrouille@dede.fr"
    update(fake_client.id, email, email=True)

    updated_client = Client.get(Client.id == fake_client.id)

    captured = capsys.readouterr()

    assert updated_client.email == email
    assert (
        f"Le champ 'Email' du client n°{fake_client.id} a été mis à jour avec succès."
        in captured.out.strip()
    )


def test_phone_update(monkey_token_check_correct_sales, fake_client, capsys):
    phone = "0669654989"
    update(fake_client.id, phone, phone=True)

    updated_client = Client.get(Client.id == fake_client.id)

    captured = capsys.readouterr()

    assert updated_client.phone == phone
    assert (
        f"Le champ 'Téléphone' du client n°{fake_client.id} a été mis à jour avec succès."
        in captured.out.strip()
    )


def test_creation_date_update(monkey_token_check_correct_sales, fake_client, capsys):
    creation_date = "2024-05-26"
    update(fake_client.id, creation_date, creation_date=True)

    updated_client = Client.get(Client.id == fake_client.id)

    captured = capsys.readouterr()

    assert updated_client.creation_date == datetime(2024, 5, 26)
    assert (
        f"Le champ 'Date de création' du client n°{fake_client.id} a été mis à jour avec succès."
        in captured.out.strip()
    )


def test_last_update_update(monkey_token_check_correct_sales, fake_client, capsys):
    last_update = "2024-07-26"
    update(fake_client.id, last_update, last_update=True)

    updated_client = Client.get(Client.id == fake_client.id)

    captured = capsys.readouterr()

    assert updated_client.last_update == datetime(2024, 7, 26)
    assert (
        f"Le champ 'Dernier contact' du client n°{fake_client.id} a été mis à jour avec succès."
        in captured.out.strip()
    )


def test_update_fails_without_attribute(
    monkey_token_check_correct_sales, fake_client, capsys
):
    with pytest.raises(Exit):
        update(fake_client.id, "Test")

    captured = capsys.readouterr()

    assert "Vous n'avez pas sélectionné d'attribut à modifier." in captured.out.strip()


def test_update_not_authorized_for_support_collaborator(
    monkey_token_check_support_gargamel, fake_client, capsys
):
    with pytest.raises(Exit):
        update(fake_client.id, "Test", name=True)

    captured = capsys.readouterr()

    assert "Action restreinte." in captured.out.strip()


def test_update_not_authorized_for_sales_collaborator(
    monkey_token_check_correct_sales_plankton, fake_client, capsys
):
    with pytest.raises(Exit):
        update(fake_client.id, "Test", name=True)

    captured = capsys.readouterr()

    assert "Action restreinte." in captured.out.strip()


def test_update_fails_without_authentication(
    monkey_token_check_false, fake_client, capsys
):
    with pytest.raises(Exit):
        update(fake_client.id, "Test", name=True)

    captured = capsys.readouterr()

    assert "Veuillez vous authentifier et réessayer." in captured.out.strip()
