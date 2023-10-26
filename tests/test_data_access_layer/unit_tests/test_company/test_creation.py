import pytest
from epicevents.data_access_layer.company import Company


def test_company_creation():
    """
    WHEN the Company.create() function is called to create a company with a valid name
    THEN the function should create a company with the provided name, and the company's name should match the provided value
    """
    name = "Test company"

    company = Company.create(name=name)

    assert company.name == name


def test_company_creation_with_wrong_name():
    """
    WHEN the Company.create() function is called to create a company with an invalid name (non-string value)
    THEN the function should raise a ValueError with an error message indicating that a valid name (string) is required
    """
    name = 1

    with pytest.raises(ValueError):
        Company.create(name=name)


def test_company_creation_with_missing_attribute():
    """
    WHEN the Company.create() function is called without specifying any attributes
    THEN the function should raise a ValueError with an error message indicating that certain attributes are required
    """
    with pytest.raises(ValueError):
        Company.create()
