import pytest
from epicevents.data_access_layer.department import Department

def test_department_creation():
    name = "Test Department"
    
    department = Department(name=name)
    
    assert department.name == name
    
def test_department_creation_with_wrong_name():
    name = 1
    
    with pytest.raises(ValueError):
        Department.create(name=name)

def test_department_creation_with_missing_attribute():
    with pytest.raises(ValueError):
        Department.create()


