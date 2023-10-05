import pytest
from datetime import datetime, timedelta, date
from peewee import IntegrityError, DataError, DoesNotExist
from epicevents.data_access_layer.contract import Contract


def test_contract_creation():
    client = 2
    collaborator = 1
    total_sum = 15399
    
    contract = Contract(
        client=client,
        collaborator =collaborator,
        total_sum=total_sum,
    )
    
    assert contract.client.id == client
    assert contract.collaborator.id == collaborator
    assert contract.total_sum == total_sum
    assert contract.amount_due == None
    assert contract.creation_date == datetime.now().date()
    assert contract.signed == False
    
def test_contract_creation_with_wrong_client_field():
    client = "Wrong"
    collaborator = 1
    total_sum = 15399
    
    with pytest.raises(DataError):
        Contract.create(
        client=client,
        collaborator =collaborator,
        total_sum=total_sum,
    )
    
def test_contract_creation_with_wrong_client_id():
    client = -12
    collaborator = 1
    total_sum = 15399
    
    with pytest.raises(DoesNotExist):
        Contract.create(
        client=client,
        collaborator =collaborator,
        total_sum=total_sum,
    )
    
def test_contract_creation_with_wrong_collaborator():
    client = 2
    collaborator = "Wrong"
    total_sum = 15399
    
    with pytest.raises(DataError):
        Contract.create(
        client=client,
        collaborator =collaborator,
        total_sum=total_sum,
    )

def test_contract_creation_with_wrong_total_sum():
    client = 2
    collaborator = 1
    total_sum = "Wrong"
    
    with pytest.raises(DataError):
        Contract.create(
        client=client,
        collaborator =collaborator,
        total_sum=total_sum,
    )
        
def test_contract_creation_with_wrong_amount_due():
    client = 2
    collaborator = 1
    total_sum = 15399
    amount_due = "Wrong"
    
    with pytest.raises(DataError):
        Contract.create(
        client=client,
        collaborator =collaborator,
        total_sum=total_sum,
        amount_due=amount_due,
    )

def test_contract_creation_with_wrong_creation_date():
    client = 2
    collaborator = 1
    total_sum = 15399
    creation_date = "Wrong"
    
    with pytest.raises(DataError):
        Contract.create(
        client=client,
        collaborator =collaborator,
        total_sum=total_sum,
        creation_date=creation_date
    )

def test_contract_creation_with_wrong_signed_field():
    client = 2
    collaborator = 1
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
        

