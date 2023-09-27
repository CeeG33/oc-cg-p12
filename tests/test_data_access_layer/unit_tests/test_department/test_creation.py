import pytest
from epicevents.data_access_layer.department import Department

def test_department_creation_successfully():
    name = "Test Department"
    
    test_department = Department.create(name=name)
    
    assert test_department.name == name
    assert test_department.id == 1
    
def test_department_creation_with_wrong_name():
    name = 1
    
    with pytest.raises(ValueError):
        Department.create(name=name)

def test_department_creation_with_missing_attribute():
    with pytest.raises(ValueError):
        Department.create()


