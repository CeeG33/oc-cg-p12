import pytest
from epicevents.cli import client
from epicevents.data_access_layer.client import Client


def test_client_create_read_and_update_successful(
    monkey_token_check_correct_sales, fake_company, capsys
):
    client.create(
        first_name="Test",
        name="Client",
        email="client@test.fr",
        phone="0654987859",
        company=fake_company.id,
    )

    created_client = Client.get(Client.email == "client@test.fr")

    assert created_client.first_name == "Test"

    client.list()

    captured = capsys.readouterr()

    assert "Tableau des clients" in captured.out.strip()

    client.update(created_client.id, "Toto", first_name=True)

    updated_client = Client.get(Client.email == "client@test.fr")

    assert updated_client.first_name == "Toto"

    updated_client.delete_instance()
