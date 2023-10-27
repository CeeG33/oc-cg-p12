import pytest
from typer import Exit
from datetime import datetime
from epicevents.data_access_layer.client import Client
from epicevents.cli.client import create


def test_creation_successful(
    monkey_token_check_correct_sales, fake_company, fake_collaborator_sales, capsys
):
    """
    Given a valid sales collaborator token, a fake company, and a fake sales collaborator,
    When a client is created with specific details,
    Then the client should be created with the expected details, including the default creation date and last update date.
    And the success message should be displayed in the captured output.
    """
    first_name = "Capitaine"
    name = "Crabs"
    email = "capitaine.crabs@ocean.com"
    phone = "0254659878"
    company = fake_company.id

    create(first_name=first_name, name=name, email=email, phone=phone, company=company)

    created_client = Client.get(Client.id == 1)

    captured = capsys.readouterr()

    assert created_client.first_name == first_name
    assert created_client.name == name
    assert created_client.email == email
    assert created_client.phone == phone
    assert created_client.company.id == company
    assert created_client.collaborator.id == fake_collaborator_sales.id
    assert created_client.creation_date.date() == datetime.now().date()
    assert created_client.last_update.date() == datetime.now().date()
    assert "Le client a été créé avec succès." in captured.out.strip()

    created_client.delete_instance()


def test_creation_with_optional_arguments_successful(
    monkey_token_check_correct_sales, fake_company, fake_collaborator_sales, capsys
):
    """
    Given a valid sales collaborator token, a fake company, and a fake sales collaborator,
    When a client is created with specific details including optional creation and last update dates,
    Then the client should be created with the expected details, including the provided creation and last update dates.
    And the success message should be displayed in the captured output.
    """
    first_name = "Capitaine"
    name = "Crabs"
    email = "capitaine.crabs@ocean.com"
    phone = "0254659878"
    company = fake_company.id
    creation_date = "2023-09-20"
    last_update = "2023-09-20"

    create(
        first_name=first_name,
        name=name,
        email=email,
        phone=phone,
        company=company,
        creation_date=creation_date,
        last_update=last_update,
    )

    created_client = Client.get(Client.id == 1)

    captured = capsys.readouterr()

    assert created_client.first_name == first_name
    assert created_client.name == name
    assert created_client.email == email
    assert created_client.phone == phone
    assert created_client.company.id == company
    assert created_client.collaborator.id == fake_collaborator_sales.id
    assert created_client.creation_date == datetime(2023, 9, 20, 0, 0)
    assert created_client.last_update == datetime(2023, 9, 20, 0, 0)
    assert "Le client a été créé avec succès." in captured.out.strip()

    created_client.delete_instance()


def test_company_not_found(monkey_token_check_correct_sales, capsys):
    """
    Given a valid sales collaborator token,
    When a client is created with an invalid company ID,
    Then an exit should be raised with an error message in the captured output.
    And no client with the same company ID should be found.
    """
    first_name = "Capitaine"
    name = "Crabs"
    email = "capitaine.crabs@ocean.com"
    phone = "0254659878"
    company = -100
    creation_date = "2023-09-20"
    last_update = "2023-09-20"

    with pytest.raises(Exit):
        create(
            first_name=first_name,
            name=name,
            email=email,
            phone=phone,
            company=company,
            creation_date=creation_date,
            last_update=last_update,
        )

    created_client = Client.get_or_none(Client.id == 1)

    captured = capsys.readouterr()

    assert f"Aucune entreprise trouvée avec l'ID n°{company}." in captured.out.strip()
    assert created_client == None


def test_creation_not_authorized(
    monkey_token_check_support_gargamel, fake_company, capsys
):
    """
    Given a valid support collaborator token and a fake company,
    When a client is created,
    Then an exit should be raised with an error message in the captured output.
    And no client should be created.
    """
    first_name = "Capitaine"
    name = "Crabs"
    email = "capitaine.crabs@ocean.com"
    phone = "0254659878"
    company = fake_company.id

    with pytest.raises(Exit):
        create(
            first_name=first_name, name=name, email=email, phone=phone, company=company
        )

    created_client = Client.get_or_none(Client.id == 1)

    captured = capsys.readouterr()

    assert "Action restreinte." in captured.out.strip()
    assert created_client == None


def test_creation_fails_if_not_authenticated(
    monkey_token_check_false, fake_company, capsys
):
    """
    Given a fake token and a fake company,
    When a client is created,
    Then an exit should be raised with an error message in the captured output.
    And no client should be created.
    """
    first_name = "Capitaine"
    name = "Crabs"
    email = "capitaine.crabs@ocean.com"
    phone = "0254659878"
    company = fake_company.id

    with pytest.raises(Exit):
        create(
            first_name=first_name, name=name, email=email, phone=phone, company=company
        )

    created_client = Client.get_or_none(Client.id == 1)

    captured = capsys.readouterr()

    assert "Veuillez vous authentifier et réessayer." in captured.out.strip()
    assert created_client == None
