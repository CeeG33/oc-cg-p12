import pytest
from epicevents.data_access_layer import collaborator

def test_collaborator_creation_successfully():
    identity = "Utilisateur Test"
    email = "test@epicevents.com"
    department = 1
    
    test_collaborator = collaborator.create_user(identity, email, department)
    
    assert test_collaborator.identity == identity
    assert test_collaborator.email == email
    assert test_collaborator.department == department
    
def test_collaborator_creation_with_wrong_identity():
    identity = "56465565"
    email = "test@epicevents.com"
    department = 1
    
    with pytest.raises(ValueError):
        collaborator.create_user(identity, email, department)
    
def test_collaborator_creation_with_wrong_email():
    identity = "Utilisateur Test"
    email = "56465565"
    department = 1
    
    with pytest.raises(ValueError):
        collaborator.create_user(identity, email, department)

def test_collaborator_creation_with_wrong_id():
    identity = "Utilisateur Test"
    email = "test@epicevents.com"
    department = 154644
    
    with pytest.raises(ValueError):
        collaborator.create_user(identity, email, department)

def test_collaborator_creation_with_missing_attribute():
    with pytest.raises(ValueError):
        collaborator.create_user()


