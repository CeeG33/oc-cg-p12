import pytest
from datetime import datetime, timedelta, date
from peewee import IntegrityError, DataError, DoesNotExist
from epicevents.data_access_layer.client import Client

def test_client_creation(fake_company, fake_collaborator):
    identity = "Client Test"
    email = "test@client.fr"
    phone = "0654987852"
    company = fake_company
    collaborator = fake_collaborator
    
    client = Client.create(
        identity=identity,
        email=email,
        phone=phone,
        company=company,
        collaborator=collaborator
    )
    
    assert client.identity == identity
    assert client.email == email
    assert client.phone == phone
    assert client.company.id == company.id
    assert client.creation_date == datetime.now().date()
    assert client.collaborator.id == collaborator.id
    
    client.delete_instance()
    
def test_client_creation_with_wrong_identity(fake_company, fake_collaborator):
    identity = "465456"
    email = "test@client.fr"
    phone = "0654987852"
    company = fake_company
    creation_date = datetime.now().date()
    last_update = None
    collaborator = fake_collaborator
    
    with pytest.raises(ValueError):
        Client.create(
        identity=identity,
        email=email,
        phone=phone,
        company=company,
        creation_date=creation_date,
        last_update=last_update,
        collaborator=collaborator
        )
    
    
def test_client_creation_with_wrong_email(fake_company, fake_collaborator):
    identity = "Client Test"
    email = "5465465"
    phone = "0654987852"
    company = fake_company
    creation_date = datetime.now().date()
    last_update = None
    collaborator = fake_collaborator
    
    with pytest.raises(ValueError):
        Client.create(
        identity=identity,
        email=email,
        phone=phone,
        company=company,
        creation_date=creation_date,
        last_update=last_update,
        collaborator=collaborator
        )

def test_client_creation_with_wrong_company_id(fake_collaborator):
    identity = "Client Test"
    email = "test@client.fr"
    phone = "0654987852"
    company = "Error"
    creation_date = datetime.now().date()
    last_update = None
    collaborator = fake_collaborator
    
    with pytest.raises(DoesNotExist):
        Client.create(
        identity=identity,
        email=email,
        phone=phone,
        company=company,
        creation_date=creation_date,
        last_update=last_update,
        collaborator=collaborator
        )

def test_client_creation_with_wrong_creation_date(fake_company, fake_collaborator):
    identity = "Client Test"
    email = "test@client.fr"
    phone = "0654987852"
    company = fake_company
    creation_date = "Error"
    last_update = None
    collaborator = fake_collaborator
    
    with pytest.raises(ValueError):
        Client.create(
        identity=identity,
        email=email,
        phone=phone,
        company=company,
        creation_date=creation_date,
        last_update=last_update,
        collaborator=collaborator
        )

def test_client_creation_with_wrong_collaborator_id(fake_company):
    identity = "Client Test"
    email = "test@client.fr"
    phone = "0654987852"
    company = fake_company
    creation_date = datetime.now().date()
    last_update = None
    collaborator = "Wrong"
    
    with pytest.raises(DoesNotExist):
        Client.create(
        identity=identity,
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
        

