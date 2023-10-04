import pytest
from datetime import datetime, timedelta, date
from peewee import IntegrityError, DataError
from epicevents.data_access_layer.contract import Contract

### ONGOING ###

def test_client_creation():
    identity = "Client Test"
    email = "test@client.fr"
    phone = "0654987852"
    company = 1
    creation_date = date.today()
    last_update = None
    collaborator = 2
    
    client = Client(
        identity=identity,
        email=email,
        phone=phone,
        company=company,
        creation_date=creation_date,
        last_update=last_update,
        collaborator=collaborator
    )
    
    assert client.identity == identity
    assert client.email == email
    assert client.phone == phone
    assert client.company.id == company
    assert client.creation_date == creation_date
    assert client.last_update == last_update
    assert client.collaborator.id == collaborator
    
def test_client_creation_with_wrong_identity():
    identity = "465456"
    email = "test@client.fr"
    phone = "0654987852"
    company = 1
    creation_date = date.today()
    last_update = None
    collaborator = 2
    
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
    
def test_client_creation_with_wrong_email():
    identity = "Client Test"
    email = "5465465"
    phone = "0654987852"
    company = 1
    creation_date = date.today()
    last_update = None
    collaborator = 2
    
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

def test_client_creation_with_wrong_company_id():
    identity = "Client Test"
    email = "test@client.fr"
    phone = "0654987852"
    company = "Error"
    creation_date = date.today()
    last_update = None
    collaborator = 2
    
    with pytest.raises(DataError):
        Client.create(
        identity=identity,
        email=email,
        phone=phone,
        company=company,
        creation_date=creation_date,
        last_update=last_update,
        collaborator=collaborator
        )

def test_client_creation_with_wrong_creation_date():
    identity = "Client Test"
    email = "test@client.fr"
    phone = "0654987852"
    company = 1
    creation_date = "Error"
    last_update = None
    collaborator = 2
    
    with pytest.raises(DataError):
        Client.create(
        identity=identity,
        email=email,
        phone=phone,
        company=company,
        creation_date=creation_date,
        last_update=last_update,
        collaborator=collaborator
        )

def test_client_creation_with_wrong_collaborator_id():
    identity = "Client Test"
    email = "test@client.fr"
    phone = "0654987852"
    company = 1
    creation_date = date.today()
    last_update = None
    collaborator = "Wrong"
    
    with pytest.raises(DataError):
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
        

