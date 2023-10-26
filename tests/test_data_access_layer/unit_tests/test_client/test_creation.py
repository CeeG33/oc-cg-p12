import pytest
from datetime import datetime
from peewee import DoesNotExist
from epicevents.data_access_layer.client import Client


def test_client_creation(fake_company, fake_collaborator_management):
    """
    GIVEN a fake company and a fake management collaborator
    WHEN the Client.create() function is called to create a client with valid attributes
    THEN the function should create a client with the provided attributes, and the client's attributes should match the provided values
    """
    first_name = "Client"
    name = "Test"
    email = "test@client.fr"
    phone = "0654987852"
    company = fake_company
    collaborator = fake_collaborator_management

    client = Client.create(
        first_name=first_name,
        name=name,
        email=email,
        phone=phone,
        company=company,
        collaborator=collaborator,
    )

    assert client.first_name == first_name
    assert client.name == name
    assert client.email == email
    assert client.phone == phone
    assert client.company.id == company.id
    assert client.creation_date == datetime.now().date()
    assert client.collaborator.id == collaborator.id

    client.delete_instance()


def test_client_creation_with_wrong_first_name(
    fake_company, fake_collaborator_management
):
    """
    GIVEN a fake company and a fake management collaborator
    WHEN the Client.create() function is called to create a client with an invalid first name
    THEN the function should raise a ValueError with an error message indicating that a valid first name is required
    """
    first_name = "465456"
    name = "Test"
    email = "test@client.fr"
    phone = "0654987852"
    company = fake_company
    creation_date = datetime.now().date()
    last_update = None
    collaborator = fake_collaborator_management

    with pytest.raises(ValueError):
        Client.create(
            first_name=first_name,
            name=name,
            email=email,
            phone=phone,
            company=company,
            creation_date=creation_date,
            last_update=last_update,
            collaborator=collaborator,
        )


def test_client_creation_with_wrong_name(fake_company, fake_collaborator_management):
    """
    GIVEN a fake company and a fake management collaborator
    WHEN the Client.create() function is called to create a client with an invalid name
    THEN the function should raise a ValueError with an error message indicating that a valid name is required
    """
    first_name = "Client"
    name = "465456"
    email = "test@client.fr"
    phone = "0654987852"
    company = fake_company
    creation_date = datetime.now().date()
    last_update = None
    collaborator = fake_collaborator_management

    with pytest.raises(ValueError):
        Client.create(
            first_name=first_name,
            name=name,
            email=email,
            phone=phone,
            company=company,
            creation_date=creation_date,
            last_update=last_update,
            collaborator=collaborator,
        )


def test_client_creation_with_wrong_email(fake_company, fake_collaborator_management):
    """
    GIVEN a fake company and a fake management collaborator
    WHEN the Client.create() function is called to create a client with an invalid email
    THEN the function should raise a ValueError with an error message indicating that a valid email is required
    """
    first_name = "Client"
    name = "Test"
    email = "5465465"
    phone = "0654987852"
    company = fake_company
    creation_date = datetime.now().date()
    last_update = None
    collaborator = fake_collaborator_management

    with pytest.raises(ValueError):
        Client.create(
            first_name=first_name,
            name=name,
            email=email,
            phone=phone,
            company=company,
            creation_date=creation_date,
            last_update=last_update,
            collaborator=collaborator,
        )


def test_client_creation_with_wrong_company_id(fake_collaborator_management):
    """
    GIVEN a fake management collaborator
    WHEN the Client.create() function is called to create a client with an invalid company ID (non-existent company)
    THEN the function should raise a DoesNotExist exception with an error message indicating that a valid company is required
    """
    first_name = "Client"
    name = "Test"
    email = "test@client.fr"
    phone = "0654987852"
    company = "Error"
    creation_date = datetime.now().date()
    last_update = None
    collaborator = fake_collaborator_management

    with pytest.raises(DoesNotExist):
        Client.create(
            first_name=first_name,
            name=name,
            email=email,
            phone=phone,
            company=company,
            creation_date=creation_date,
            last_update=last_update,
            collaborator=collaborator,
        )


def test_client_creation_with_wrong_creation_date(
    fake_company, fake_collaborator_management
):
    """
    GIVEN a fake company and a fake management collaborator
    WHEN the Client.create() function is called to create a client with an invalid creation date (non-date value)
    THEN the function should raise a ValueError with an error message indicating that a valid creation date is required
    """
    first_name = "Client"
    name = "Test"
    email = "test@client.fr"
    phone = "0654987852"
    company = fake_company
    creation_date = "Error"
    last_update = None
    collaborator = fake_collaborator_management

    with pytest.raises(ValueError):
        Client.create(
            first_name=first_name,
            name=name,
            email=email,
            phone=phone,
            company=company,
            creation_date=creation_date,
            last_update=last_update,
            collaborator=collaborator,
        )


def test_client_creation_with_wrong_collaborator_id(fake_company):
    """
    GIVEN a fake company
    WHEN the Client.create() function is called to create a client with an invalid collaborator ID (non-existent collaborator)
    THEN the function should raise a DoesNotExist exception with an error message indicating that a valid collaborator is required
    """
    first_name = "Client"
    name = "Test"
    email = "test@client.fr"
    phone = "0654987852"
    company = fake_company
    creation_date = datetime.now().date()
    last_update = None
    collaborator = "Wrong"

    with pytest.raises(DoesNotExist):
        Client.create(
            first_name=first_name,
            name=name,
            email=email,
            phone=phone,
            company=company,
            creation_date=creation_date,
            last_update=last_update,
            collaborator=collaborator,
        )


def test_collaborator_creation_with_missing_attribute():
    """
    WHEN the Client.create() function is called without specifying any attributes
    THEN the function should raise a ValueError with an error message indicating that certain attributes are required
    """
    with pytest.raises(ValueError):
        Client.create()
