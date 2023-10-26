import pytest
from epicevents.data_access_layer.department import Department


def test_department_creation():
    """
    GIVEN a valid department name
    WHEN the Department class is instantiated
    THEN the department object should have a name attribute matching the provided name.
    """
    name = "Test Department"

    department = Department(name=name)

    assert department.name == name


def test_department_creation_with_wrong_name():
    """
    GIVEN an invalid department name (non-string type)
    WHEN attempting to create a Department object
    THEN the creation should raise a ValueError with an appropriate error message.
    """
    name = 1

    with pytest.raises(ValueError):
        Department.create(name=name)


def test_department_creation_with_missing_attribute():
    """
    GIVEN no attributes provided (an empty state)
    WHEN attempting to create a Department object
    THEN the creation should raise a ValueError because the name attribute is missing.
    """
    with pytest.raises(ValueError):
        Department.create()
