import pytest
from datetime import datetime, timedelta, timezone
from peewee import IntegrityError
from argon2 import PasswordHasher
from epicevents.data_access_layer.collaborator import Collaborator
from epicevents.data_access_layer.department import Department
from epicevents.cli.collaborator import MANAGEMENT_DEPARTMENT_ID


def test_collaborator_creation(fake_department_management):
    """
    GIVEN a fake management department
    WHEN the Collaborator.create() function is called to create a collaborator with valid attributes
    THEN the function should create a collaborator with the provided attributes, and the collaborator's attributes should match the provided values
    """
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
        department=department,
    )

    assert collaborator.first_name == first_name
    assert collaborator.name == name
    assert collaborator.email == email
    assert collaborator.department.id == department
    assert collaborator.password != password


def test_collaborator_creation_with_wrong_first_name():
    """
    GIVEN a fake management department
    WHEN the Collaborator.create() function is called to create a collaborator with an invalid first name (non-alphabetical characters)
    THEN the function should raise a ValueError with an error message indicating that a valid first name is required
    """
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
            department=department,
        )


def test_collaborator_creation_with_wrong_name():
    """
    GIVEN a fake management department
    WHEN the Collaborator.create() function is called to create a collaborator with an invalid name (non-alphabetical characters)
    THEN the function should raise a ValueError with an error message indicating that a valid name is required
    """
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
            department=department,
        )


def test_collaborator_creation_with_wrong_email():
    """
    GIVEN a fake management department
    WHEN the Collaborator.create() function is called to create a collaborator with an invalid email
    THEN the function should raise a ValueError with an error message indicating that a valid email is required
    """
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
            department=department,
        )


def test_collaborator_creation_with_wrong_department_id():
    """
    GIVEN a fake management department
    WHEN the Collaborator.create() function is called to create a collaborator with an invalid department ID (non-existent department)
    THEN the function should raise an IntegrityError with an error message indicating that a valid department is required
    """
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
            department=department,
        )


def test_collaborator_creation_with_missing_attribute():
    """
    GIVEN a fake management department
    WHEN the Collaborator.create() function is called without specifying any attributes
    THEN the function should raise a ValueError with an error message indicating that certain attributes are required
    """
    with pytest.raises(ValueError):
        Collaborator.create()


def test_collaborator_get_data(fake_department_sales):
    """
    GIVEN a fake sales department
    WHEN the Collaborator.create() function is called to create a collaborator with valid attributes
    THEN the collaborator's get_data() method should return a dictionary with specific collaborator's attributes and values
    """
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
        department=department,
    )

    collaborator_data = collaborator.get_data()

    expected_result = {
        "collaborator_id": f"{collaborator.id}",
        "email": f"{collaborator.email}",
        "department_id": f"{collaborator.department.id}",
        "exp": datetime.now(tz=timezone.utc) + timedelta(hours=1),
    }

    assert collaborator_data == expected_result
