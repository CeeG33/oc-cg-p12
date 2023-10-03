import pytest
from epicevents.data_access_layer.collaborator import Collaborator

def test_collaborator_creation_successfully():
    identity = "Utilisateur Test"
    email = "test@epicevents.com"
    password = "password"
    department = 1
    
    test_collaborator = Collaborator.create(identity=identity, email=email, password=password, department=department)
    
    assert test_collaborator.identity == identity
    assert test_collaborator.email == email
    assert test_collaborator.department.id == department
    
def test_collaborator_creation_with_wrong_identity():
    identity = "56465565"
    email = "test@epicevents.com"
    password = "password"
    department = 1
    
    with pytest.raises(ValueError):
        Collaborator.create(identity=identity, email=email, password=password, department=department)
    
def test_collaborator_creation_with_wrong_email():
    identity = "Utilisateur Test"
    email = "56465565"
    password = "password"
    department = 1
    
    with pytest.raises(ValueError):
        Collaborator.create(identity=identity, email=email, password=password, department=department)

def test_collaborator_creation_with_wrong_id():
    identity = "Utilisateur Test"
    email = "test@epicevents.com"
    password = "password"
    department = 154644
    
    with pytest.raises(ValueError):
        Collaborator.create(identity=identity, email=email, password=password, department=department)

def test_collaborator_creation_with_missing_attribute():
    with pytest.raises(ValueError):
        Collaborator.create()


