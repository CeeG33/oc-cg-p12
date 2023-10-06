import pytest
from datetime import datetime, timedelta, date
from peewee import IntegrityError, DataError, DoesNotExist
from epicevents.data_access_layer.event import Event


def test_event_creation(fake_contract, fake_collaborator):
    contract = fake_contract
    start_date = "2023-02-05 14:30"
    end_date = "2023-02-05 20:30"
    location = "54, avenue des Agneaux, 77500 CRO-MAGNON"
    attendees = 8
    notes = "Quelques notes..."
    support = fake_collaborator
    
    event = Event.create(
        contract=contract,
        start_date=start_date,
        end_date=end_date,
        location=location,
        attendees=attendees,
        notes=notes,
        support=support,
    )
    
    assert event.contract.id == contract.id
    assert event.start_date == start_date
    assert event.end_date == end_date
    assert event.location == location
    assert event.attendees == attendees
    assert event.notes == notes
    assert event.support.id == support.id
    
def test_event_creation_with_wrong_contract_field(fake_collaborator):
    contract = "Wrong"
    start_date = "2023-02-05 14:30"
    end_date = "2023-02-05 20:30"
    location = "54, avenue des Agneaux, 77500 CRO-MAGNON"
    attendees = 8
    notes = "Quelques notes..."
    support = fake_collaborator
    
    with pytest.raises(DoesNotExist):
        Event.create(
        contract=contract,
        start_date=start_date,
        end_date=end_date,
        location=location,
        attendees=attendees,
        notes=notes,
        support=support,
    )
    
def test_event_creation_with_wrong_contract_id(fake_collaborator):
    contract = -12
    start_date = "2023-02-05 14:30"
    end_date = "2023-02-05 20:30"
    location = "54, avenue des Agneaux, 77500 CRO-MAGNON"
    attendees = 8
    notes = "Quelques notes..."
    support = fake_collaborator
    
    with pytest.raises(DoesNotExist):
        Event.create(
        contract=contract,
        start_date=start_date,
        end_date=end_date,
        location=location,
        attendees=attendees,
        notes=notes,
        support=support,
    )
    
def test_event_creation_with_wrong_collaborator(fake_client):
    contract = 1
    start_date = "2023-02-05 14:30"
    end_date = "2023-02-05 20:30"
    location = "54, avenue des Agneaux, 77500 CRO-MAGNON"
    attendees = 8
    notes = "Quelques notes..."
    support = "Wrong"
    
    with pytest.raises(DoesNotExist):
        Event.create(
        contract=contract,
        start_date=start_date,
        end_date=end_date,
        location=location,
        attendees=attendees,
        notes=notes,
        support=support,
    )

def test_event_creation_with_wrong_collaborator_id(fake_client):
    contract = 1
    start_date = "2023-02-05 14:30"
    end_date = "2023-02-05 20:30"
    location = "54, avenue des Agneaux, 77500 CRO-MAGNON"
    attendees = 8
    notes = "Quelques notes..."
    support = -12
    
    with pytest.raises(DoesNotExist):
        Event.create(
        contract=contract,
        start_date=start_date,
        end_date=end_date,
        location=location,
        attendees=attendees,
        notes=notes,
        support=support,
    )

def test_event_creation_with_wrong_total_sum(fake_client, fake_collaborator):
    client = fake_client
    collaborator = fake_collaborator
    total_sum = "Wrong"
    
    with pytest.raises(ValueError):
        Event.create(
        client=client,
        collaborator =collaborator,
        total_sum=total_sum,
    )
        
def test_event_creation_with_wrong_amount_due(fake_client, fake_collaborator):
    client = fake_client
    collaborator = fake_collaborator
    total_sum = 15399
    amount_due = "Wrong"
    
    with pytest.raises(ValueError):
        Event.create(
        client=client,
        collaborator =collaborator,
        total_sum=total_sum,
        amount_due=amount_due,
    )

def test_event_creation_with_wrong_creation_date(fake_client, fake_collaborator):
    client = fake_client
    collaborator = fake_collaborator
    total_sum = 15399
    creation_date = "Wrong"
    
    with pytest.raises(ValueError):
        Event.create(
        client=client,
        collaborator =collaborator,
        total_sum=total_sum,
        creation_date=creation_date
    )

def test_event_creation_with_wrong_signed_field(fake_client, fake_collaborator):
    client = fake_client
    collaborator = fake_collaborator
    total_sum = 15399
    signed = "Wrong"
    
    with pytest.raises(ValueError):
        Event.create(
        client=client,
        collaborator =collaborator,
        total_sum=total_sum,
        signed=signed
    )

def test_collaborator_creation_with_missing_attribute():
    with pytest.raises(DoesNotExist):
        Event.create()
        

