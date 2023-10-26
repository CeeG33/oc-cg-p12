import pytest
from datetime import datetime, timedelta, date
from peewee import IntegrityError, DataError, DoesNotExist
from epicevents.data_access_layer.contract import Contract


def test_contract_creation(fake_client, fake_collaborator_sales):
    """
    WHEN the Contract.create() function is called to create a contract with valid input values
    THEN the function should create a contract with the provided client, collaborator, total_sum, and default values for other attributes.
    AND the contract's attributes should match the provided values.
    """
    client = fake_client.id
    collaborator = fake_collaborator_sales.id
    total_sum = 15399

    contract = Contract.create(
        client=client,
        collaborator=collaborator,
        total_sum=total_sum,
    )

    assert contract.client.id == client
    assert contract.collaborator.id == collaborator
    assert contract.total_sum == total_sum
    assert contract.amount_due == None
    assert contract.creation_date == datetime.now().date()
    assert contract.signed == False


def test_contract_creation_with_wrong_client_field(fake_collaborator_sales):
    """
    WHEN the Contract.create() function is called to create a contract with an invalid client field (non-existent client)
    THEN the function should raise a DoesNotExist exception with an error message indicating that a valid client is required.
    """
    client = "Wrong"
    collaborator = fake_collaborator_sales.id
    total_sum = 15399

    with pytest.raises(DoesNotExist):
        Contract.create(
            client=client,
            collaborator=collaborator,
            total_sum=total_sum,
        )


def test_contract_creation_with_wrong_client_id(fake_collaborator_sales):
    """
    WHEN the Contract.create() function is called to create a contract with an invalid client ID (negative value)
    THEN the function should raise a DoesNotExist exception with an error message indicating that a valid client is required.
    """
    client = -12
    collaborator = fake_collaborator_sales.id
    total_sum = 15399

    with pytest.raises(DoesNotExist):
        Contract.create(
            client=client,
            collaborator=collaborator,
            total_sum=total_sum,
        )


def test_contract_creation_with_wrong_collaborator(fake_client):
    """
    WHEN the Contract.create() function is called to create a contract with an invalid collaborator field (non-existent collaborator)
    THEN the function should raise a DoesNotExist exception with an error message indicating that a valid collaborator is required.
    """
    client = fake_client.id
    collaborator = "Wrong"
    total_sum = 15399

    with pytest.raises(DoesNotExist):
        Contract.create(
            client=client,
            collaborator=collaborator,
            total_sum=total_sum,
        )


def test_contract_creation_with_wrong_total_sum(fake_client, fake_collaborator_sales):
    """
    WHEN the Contract.create() function is called to create a contract with an invalid total_sum (non-numeric value)
    THEN the function should raise a ValueError with an error message indicating that a valid total_sum is required.
    """
    client = fake_client.id
    collaborator = fake_collaborator_sales.id
    total_sum = "Wrong"

    with pytest.raises(ValueError):
        Contract.create(
            client=client,
            collaborator=collaborator,
            total_sum=total_sum,
        )


def test_contract_creation_with_wrong_amount_due(fake_client, fake_collaborator_sales):
    """
    WHEN the Contract.create() function is called to create a contract with an invalid amount_due (non-numeric value)
    THEN the function should raise a ValueError with an error message indicating that a valid amount_due is required.
    """
    client = fake_client.id
    collaborator = fake_collaborator_sales.id
    total_sum = 15399
    amount_due = "Wrong"

    with pytest.raises(ValueError):
        Contract.create(
            client=client,
            collaborator=collaborator,
            total_sum=total_sum,
            amount_due=amount_due,
        )


def test_contract_creation_with_wrong_creation_date(
    fake_client, fake_collaborator_sales
):
    """
    WHEN the Contract.create() function is called to create a contract with an invalid creation_date (non-date format)
    THEN the function should raise a ValueError with an error message indicating that a valid creation date is required.
    """
    client = fake_client.id
    collaborator = fake_collaborator_sales.id
    total_sum = 15399
    creation_date = "Wrong"

    with pytest.raises(ValueError):
        Contract.create(
            client=client,
            collaborator=collaborator,
            total_sum=total_sum,
            creation_date=creation_date,
        )


def test_contract_creation_with_wrong_signed_field(
    fake_client, fake_collaborator_sales
):
    """
    WHEN the Contract.create() function is called to create a contract with an invalid signed field (non-boolean value)
    THEN the function should raise a ValueError with an error message indicating that a valid signed value is required.
    """
    client = fake_client.id
    collaborator = fake_collaborator_sales.id
    total_sum = 15399
    signed = "Wrong"

    with pytest.raises(ValueError):
        Contract.create(
            client=client, collaborator=collaborator, total_sum=total_sum, signed=signed
        )


def test_collaborator_creation_with_missing_attribute():
    """
    WHEN the Contract.create() function is called without specifying any attributes
    THEN the function should raise a DoesNotExist exception with an error message indicating that certain attributes are required.
    """
    with pytest.raises(DoesNotExist):
        Contract.create()
