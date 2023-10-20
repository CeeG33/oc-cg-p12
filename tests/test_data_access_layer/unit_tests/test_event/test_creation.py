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
    
def test_event_creation_with_no_support(fake_contract):
    contract = fake_contract
    start_date = "2023-02-05 14:30"
    end_date = "2023-02-05 20:30"
    location = "54, avenue des Agneaux, 77500 CRO-MAGNON"
    attendees = 8
    notes = "Quelques notes..."
    
    event = Event.create(
        contract=contract,
        start_date=start_date,
        end_date=end_date,
        location=location,
        attendees=attendees,
        notes=notes
    )
    
    assert event.contract.id == contract.id
    assert event.start_date == start_date
    assert event.end_date == end_date
    assert event.location == location
    assert event.attendees == attendees
    assert event.notes == notes
    assert event.support == None

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

def test_event_creation_with_wrong_collaborator(fake_contract):
    contract = fake_contract
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

def test_event_creation_with_wrong_collaborator_id(fake_contract):
    contract = fake_contract
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

def test_event_creation_with_wrong_start_date(fake_contract, fake_collaborator):
    contract = fake_contract
    start_date = "Wrong"
    end_date = "2023-02-05 20:30"
    location = "54, avenue des Agneaux, 77500 CRO-MAGNON"
    attendees = 8
    notes = "Quelques notes..."
    support = fake_collaborator
    
    with pytest.raises(ValueError):
        Event.create(
        contract=contract,
        start_date=start_date,
        end_date=end_date,
        location=location,
        attendees=attendees,
        notes=notes,
        support=support,
    )

def test_event_creation_with_wrong_end_date(fake_contract, fake_collaborator):
    contract = fake_contract
    start_date = "2023-02-05 20:30"
    end_date = "Wrong"
    location = "54, avenue des Agneaux, 77500 CRO-MAGNON"
    attendees = 8
    notes = "Quelques notes..."
    support = fake_collaborator
    
    with pytest.raises(ValueError):
        Event.create(
        contract=contract,
        start_date=start_date,
        end_date=end_date,
        location=location,
        attendees=attendees,
        notes=notes,
        support=support,
    )

def test_event_creation_with_no_start_date(fake_contract, fake_collaborator):
    contract = fake_contract
    end_date = "Wrong"
    location = "54, avenue des Agneaux, 77500 CRO-MAGNON"
    attendees = 8
    notes = "Quelques notes..."
    support = fake_collaborator
    
    with pytest.raises(ValueError):
        Event.create(
        contract=contract,
        end_date=end_date,
        location=location,
        attendees=attendees,
        notes=notes,
        support=support,
    )

def test_event_creation_with_no_end_date(fake_contract, fake_collaborator):
    contract = fake_contract
    start_date = "2023-02-05 20:30"
    location = "54, avenue des Agneaux, 77500 CRO-MAGNON"
    attendees = 8
    notes = "Quelques notes..."
    support = fake_collaborator
    
    with pytest.raises(ValueError):
        Event.create(
        contract=contract,
        start_date=start_date,
        location=location,
        attendees=attendees,
        notes=notes,
        support=support,
    )

def test_event_creation_with_no_location(fake_contract, fake_collaborator):
    contract = fake_contract
    start_date = "2023-02-05 14:30"
    end_date = "2023-02-05 20:30"
    attendees = 8
    notes = "Quelques notes..."
    support = fake_collaborator
    
    with pytest.raises(ValueError):
        Event.create(
        contract=contract,
        start_date=start_date,
        end_date=end_date,
        attendees=attendees,
        notes=notes,
        support=support,
    )

def test_event_creation_with_wrong_attendees_value(fake_contract, fake_collaborator):
    contract = fake_contract
    start_date = "2023-02-05 14:30"
    end_date = "2023-02-05 20:30"
    location = "54, avenue des Agneaux, 77500 CRO-MAGNON"
    attendees = "Wrong"
    notes = "Quelques notes..."
    support = fake_collaborator
    
    with pytest.raises(ValueError):
        Event.create(
        contract=contract,
        start_date=start_date,
        end_date=end_date,
        location=location,
        attendees=attendees,
        notes=notes,
        support=support,
    )

def test_event_creation_with_negative_attendees_value(fake_contract, fake_collaborator):
    contract = fake_contract
    start_date = "2023-02-05 14:30"
    end_date = "2023-02-05 20:30"
    location = "54, avenue des Agneaux, 77500 CRO-MAGNON"
    attendees = -1
    notes = "Quelques notes..."
    support = fake_collaborator
    
    with pytest.raises(ValueError):
        Event.create(
        contract=contract,
        start_date=start_date,
        end_date=end_date,
        location=location,
        attendees=attendees,
        notes=notes,
        support=support,
    )

###CHECKKK
# def test_event_creation_with_number_instead_of_location(fake_contract, fake_collaborator):
#     contract = fake_contract
#     start_date = "2023-02-05 14:30"
#     end_date = "2023-02-05 20:30"
#     location = "54, avenue des Agneaux, 77500 CRO-MAGNON"
#     attendees = 8
#     notes = "Quelques notes..."
#     support = fake_collaborator
    
#     with pytest.raises(ValueError):
#         Event.create(
#         contract=contract,
#         start_date=start_date,
#         end_date=end_date,
#         location=location,
#         attendees=attendees,
#         notes=notes,
#         support=support,
#     )

def test_event_creation_with_missing_attribute():
    with pytest.raises(DoesNotExist):
        Event.create()


