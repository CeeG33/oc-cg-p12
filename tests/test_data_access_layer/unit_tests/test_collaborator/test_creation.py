import pytest
from datetime import datetime, timedelta, timezone
from peewee import IntegrityError
from argon2 import PasswordHasher
from epicevents.data_access_layer.collaborator import Collaborator
from epicevents.data_access_layer.department import Department
from epicevents.cli.collaborator import MANAGEMENT_DEPARTMENT_ID

def test_collaborator_creation(fake_department_management):
    first_name = "Utilisateur"
    name = "Test"
    email = "test@epicevents.com"
    password = "password"
    department = MANAGEMENT_DEPARTMENT_ID
    
    collaborator = Collaborator.create(
        first_name=first_name,
        name=name, 
        email=email, 
        password=password, 
        department=department
    )
    
    assert collaborator.first_name == first_name
    assert collaborator.name == name
    assert collaborator.email == email
    assert collaborator.department.id == department
    assert collaborator.password != password
    
def test_collaborator_creation_with_wrong_first_name():
    first_name = "56465565"
    name = "Test"
    email = "test@epicevents.com"
    password = "password"
    department = MANAGEMENT_DEPARTMENT_ID
    
    with pytest.raises(ValueError):
        Collaborator.create(
            first_name=first_name,
            name=name,  
            email=email, 
            password=password, 
            department=department
        )

def test_collaborator_creation_with_wrong_name():
    first_name = "Utilisateur"
    name = "56465565"
    email = "test@epicevents.com"
    password = "password"
    department = MANAGEMENT_DEPARTMENT_ID
    
    with pytest.raises(ValueError):
        Collaborator.create(
            first_name=first_name,
            name=name,  
            email=email, 
            password=password, 
            department=department
        )

def test_collaborator_creation_with_wrong_email():
    first_name = "Utilisateur"
    name = "Test"
    email = "56465565"
    password = "password"
    department = MANAGEMENT_DEPARTMENT_ID
    
    with pytest.raises(ValueError):
        Collaborator.create(
            first_name=first_name,
            name=name, 
            email=email, 
            password=password, 
            department=department
        )

def test_collaborator_creation_with_wrong_department_id():
    first_name = "Utilisateur"
    name = "Test"
    email = "test@epicevents.com"
    password = "password"
    department = 154644
    
    with pytest.raises(IntegrityError):
        Collaborator.create(
            first_name=first_name,
            name=name,
            email=email,
            password=password,
            department=department
        )

def test_collaborator_creation_with_missing_attribute():
    with pytest.raises(ValueError):
        Collaborator.create()

def test_collaborator_get_data(fake_department_management):
    first_name = "Utilisateur"
    name = "Test"
    email = "testing@epicevents.com"
    password = "password"
    department = MANAGEMENT_DEPARTMENT_ID
    
    collaborator = Collaborator.create(
        first_name=first_name,
        name=name, 
        email=email,
        password=password,
        department=department
    )
    
    expected_result = {
            "collaborator_id" : f"{collaborator.id}",
            "email": f"{collaborator.email}",
            "department_id": f"{collaborator.department.id}",
            "exp": datetime.now(tz=timezone.utc) + timedelta(hours=1) 
        }
    
    assert collaborator.get_data() == expected_result
