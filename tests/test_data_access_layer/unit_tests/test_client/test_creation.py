import pytest
from datetime import datetime
from peewee import DoesNotExist
from epicevents.data_access_layer.client import Client

def test_client_creation(fake_company, fake_collaborator_management):
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
        collaborator=collaborator
    )
    
    assert client.first_name == first_name
    assert client.name == name
    assert client.email == email
    assert client.phone == phone
    assert client.company.id == company.id
    assert client.creation_date == datetime.now().date()
    assert client.collaborator.id == collaborator.id
    
    client.delete_instance()
    
def test_client_creation_with_wrong_first_name(fake_company, fake_collaborator_management):
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
        collaborator=collaborator
        )
    
def test_client_creation_with_wrong_name(fake_company, fake_collaborator_management):
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
        collaborator=collaborator
        )
    
def test_client_creation_with_wrong_email(fake_company, fake_collaborator_management):
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
        collaborator=collaborator
        )

def test_client_creation_with_wrong_company_id(fake_collaborator_management):
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
        collaborator=collaborator
        )

def test_client_creation_with_wrong_creation_date(fake_company, fake_collaborator_management):
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
        collaborator=collaborator
        )

def test_client_creation_with_wrong_collaborator_id(fake_company):
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
        collaborator=collaborator
        )

def test_collaborator_creation_with_missing_attribute():
    with pytest.raises(ValueError):
        Client.create()
        

