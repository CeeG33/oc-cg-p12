import pytest
from epicevents.data_access_layer.company import Company

def test_company_creation():
    name = "Test company"
    
    company = Company.create(name=name)
    
    assert company.name == name
    
def test_company_creation_with_wrong_name():
    name = 1
    
    with pytest.raises(ValueError):
        Company.create(name=name)

def test_company_creation_with_missing_attribute():
    with pytest.raises(ValueError):
        Company.create()


