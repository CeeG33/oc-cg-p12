import pytest
from datetime import datetime, timedelta
from peewee import IntegrityError
from argon2 import PasswordHasher
from epicevents.data_access_layer.collaborator import Collaborator
from epicevents.data_access_layer.department import Department

def test_collaborator_creation(fake_department):
    identity = "Utilisateur Test"
    email = "test@epicevents.com"
    password = "password"
    department = fake_department
    
    collaborator = Collaborator.create(
        identity=identity, 
        email=email, 
        password=password, 
        department=department
    )
    
    assert collaborator.identity == identity
    assert collaborator.email == email
    assert collaborator.department.id == department.id
    assert collaborator.password != password
    
def test_collaborator_creation_with_wrong_identity(fake_department):
    identity = "56465565"
    email = "test@epicevents.com"
    password = "password"
    department = fake_department
    
    with pytest.raises(ValueError):
        Collaborator.create(
            identity=identity, 
            email=email, 
            password=password, 
            department=department
        )
    
def test_collaborator_creation_with_wrong_email(fake_department):
    identity = "Utilisateur Test"
    email = "56465565"
    password = "password"
    department = fake_department
    
    with pytest.raises(ValueError):
        Collaborator.create(
            identity=identity, 
            email=email, 
            password=password, 
            department=department
        )

def test_collaborator_creation_with_wrong_department_id():
    identity = "Utilisateur Test"
    email = "test@epicevents.com"
    password = "password"
    department = 154644
    
    with pytest.raises(IntegrityError):
        Collaborator.create(
            identity=identity, 
            email=email, 
            password=password, 
            department=department
        )

def test_collaborator_creation_with_missing_attribute():
    with pytest.raises(ValueError):
        Collaborator.create()

def test_collaborator_get_data(fake_department):
    identity = "Utilisateur Testtest"
    email = "testing@epicevents.com"
    password = "password"
    department = fake_department
    
    collaborator = Collaborator.create(
        identity=identity, 
        email=email, 
        password=password, 
        department=department
    )
    
    expected_result = {
            "collaborator_id" : f"{collaborator.id}",
            "email": f"{collaborator.email}",
            "department_id": f"{collaborator.department}",
            "exp": datetime.utcnow() + timedelta(hours=1) 
        }
    
    assert collaborator.get_data() == expected_result
