import pytest
from typer import Exit
from datetime import datetime
from epicevents.data_access_layer.contract import Contract
from epicevents.cli.contract import create
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError


def test_creation_successful(
    monkey_token_check_management, fake_client, fake_collaborator_sales, capsys
):
    client = fake_client
    collaborator = fake_collaborator_sales
    create(client=client.id, collaborator=collaborator.id, total_sum=30000)

    created_contract = Contract.get(Contract.total_sum == 30000)

    captured = capsys.readouterr()

    assert created_contract.client.id == client.id
    assert created_contract.collaborator.id == collaborator.id
    assert created_contract.total_sum == 30000.00
    assert created_contract.amount_due == None
    assert created_contract.creation_date.date() == datetime.now().date()
    assert created_contract.signed == False
    assert "Le contrat a été créé avec succès." in captured.out.strip()

    created_contract.delete_instance()


def test_creation_with_optional_arguments_successful(
    monkey_token_check_management, fake_client, fake_collaborator_sales, capsys
):
    client = fake_client
    collaborator = fake_collaborator_sales
    create(
        client=client.id,
        collaborator=collaborator.id,
        total_sum=15000,
        amount_due=15000,
        creation_date="2023-10-15",
        signed=True,
    )

    created_contract = Contract.get(Contract.total_sum == 15000)

    captured = capsys.readouterr()

    assert created_contract.client.id == client.id
    assert created_contract.collaborator.id == collaborator.id
    assert created_contract.total_sum == 15000.00
    assert created_contract.amount_due == 15000.00
    assert created_contract.creation_date.date() == datetime(2023, 10, 15).date()
    assert created_contract.signed == True
    assert "Le contrat a été créé avec succès." in captured.out.strip()

    created_contract.delete_instance()

def test_creation_fails_with_wrong_client_id(
    monkey_token_check_management, fake_collaborator_sales, capsys
):
    client = -100
    collaborator = fake_collaborator_sales
    with pytest.raises(Exit):
        create(client=client, collaborator=collaborator.id, total_sum=30000)

    created_contract = Contract.get_or_none(Contract.client == client)

    captured = capsys.readouterr()

    assert created_contract == None
    assert f"Aucun client trouvé avec l'ID n°{client}." in captured.out.strip()


def test_creation_fails_with_wrong_collaborator_id(
    monkey_token_check_management, fake_client, capsys
):
    client = fake_client
    collaborator = -100
    with pytest.raises(Exit):
        create(client=client.id, collaborator=collaborator, total_sum=30000)

    created_contract = Contract.get_or_none(Contract.collaborator == collaborator)

    captured = capsys.readouterr()

    assert created_contract == None
    assert f"Aucun commercial trouvé avec l'ID n°{collaborator}." in captured.out.strip()


def test_creation_not_authorized(
    monkey_token_check_correct_sales, fake_client, fake_collaborator_sales, capsys
):
    client = fake_client
    collaborator = fake_collaborator_sales
    with pytest.raises(Exit):
        create(
            client=client.id,
            collaborator=collaborator.id,
            total_sum=23000,
            amount_due=15000,
            creation_date="2023-10-15",
            signed=True,
        )

    created_contract = Contract.get_or_none(Contract.total_sum == 23000)

    captured = capsys.readouterr()

    assert created_contract == None
    assert "Action restreinte." in captured.out.strip()


def test_creation_fails_if_not_authenticated(
    monkey_token_check_false, fake_client, fake_collaborator_sales, capsys
):
    client = fake_client
    collaborator = fake_collaborator_sales
    with pytest.raises(Exit):
        create(
            client=client.id,
            collaborator=collaborator.id,
            total_sum=14000,
            amount_due=15000,
            creation_date="2023-10-15",
            signed=True,
        )

    created_contract = Contract.get_or_none(Contract.total_sum == 14000)

    captured = capsys.readouterr()

    assert created_contract == None
    assert "Veuillez vous authentifier et réessayer." in captured.out.strip()
