import pytest
from datetime import datetime, timedelta, date
from peewee import IntegrityError, DataError, DoesNotExist
from epicevents.data_access_layer.contract import Contract


def test_contract_creation(fake_client, fake_collaborator):
    client = fake_client
    collaborator = fake_collaborator
    total_sum = 15399
    
    contract = Contract.create(
        client=client,
        collaborator =collaborator,
        total_sum=total_sum,
    )
    
    assert contract.client.id == client.id
    assert contract.collaborator.id == collaborator.id
    assert contract.total_sum == Contract()._format_number(total_sum)
    assert contract.amount_due == None
    assert contract.creation_date == datetime.now().date()
    assert contract.signed == False
    
def test_contract_creation_with_wrong_client_field(fake_collaborator):
    client = "Wrong"
    collaborator = fake_collaborator
    total_sum = 15399
    
    with pytest.raises(DoesNotExist):
        Contract.create(
        client=client,
        collaborator =collaborator,
        total_sum=total_sum,
    )
    
def test_contract_creation_with_wrong_client_id(fake_collaborator):
    client = -12
    collaborator = fake_collaborator
    total_sum = 15399
    
    with pytest.raises(DoesNotExist):
        Contract.create(
        client=client,
        collaborator =collaborator,
        total_sum=total_sum,
    )
    
def test_contract_creation_with_wrong_collaborator(fake_client):
    client = fake_client
    collaborator = "Wrong"
    total_sum = 15399
    
    with pytest.raises(DoesNotExist):
        Contract.create(
        client=client,
        collaborator =collaborator,
        total_sum=total_sum,
    )

def test_contract_creation_with_wrong_total_sum(fake_client, fake_collaborator):
    client = fake_client
    collaborator = fake_collaborator
    total_sum = "Wrong"
    
    with pytest.raises(ValueError):
        Contract.create(
        client=client,
        collaborator =collaborator,
        total_sum=total_sum,
    )
        
def test_contract_creation_with_wrong_amount_due(fake_client, fake_collaborator):
    client = fake_client
    collaborator = fake_collaborator
    total_sum = 15399
    amount_due = "Wrong"
    
    with pytest.raises(ValueError):
        Contract.create(
        client=client,
        collaborator =collaborator,
        total_sum=total_sum,
        amount_due=amount_due,
    )

def test_contract_creation_with_wrong_creation_date(fake_client, fake_collaborator):
    client = fake_client
    collaborator = fake_collaborator
    total_sum = 15399
    creation_date = "Wrong"
    
    with pytest.raises(ValueError):
        Contract.create(
        client=client,
        collaborator =collaborator,
        total_sum=total_sum,
        creation_date=creation_date
    )

def test_contract_creation_with_wrong_signed_field(fake_client, fake_collaborator):
    client = fake_client
    collaborator = fake_collaborator
    total_sum = 15399
    signed = "Wrong"
    
    with pytest.raises(ValueError):
        Contract.create(
        client=client,
        collaborator =collaborator,
        total_sum=total_sum,
        signed=signed
    )

def test_collaborator_creation_with_missing_attribute():
    with pytest.raises(DoesNotExist):
        Contract.create()
        

