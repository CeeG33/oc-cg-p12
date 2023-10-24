import pytest, os, jwt
import sentry_sdk
from datetime import datetime, timedelta
from peewee import PostgresqlDatabase, SqliteDatabase
from dotenv import load_dotenv, find_dotenv
from epicevents.data_access_layer import (
    client,
    collaborator,
    company,
    contract,
    department,
    event,
)
from epicevents.data_access_layer import database
from epicevents.cli import collaborator as clicollaborator
from epicevents.cli import contract as clicontract
from epicevents.cli.collaborator import (
    SECRET_KEY,
    MANAGEMENT_DEPARTMENT_ID,
    SALES_DEPARTMENT_ID,
    SUPPORT_DEPARTMENT_ID,
)

MODELS = [
    client.Client,
    collaborator.Collaborator,
    company.Company,
    contract.Contract,
    department.Department,
    event.Event,
]

test_db = SqliteDatabase(":memory:")
test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
test_db.connect()
test_db.create_tables(MODELS)


@pytest.fixture(autouse=True)
def test_database(monkeypatch):
    mocked_database = monkeypatch.setattr(database, "psql_db", test_db)
    return mocked_database


@pytest.fixture()
def fake_department_management():
    fake_department1 = department.Department.create(name="Management")
    fake_department1.id = MANAGEMENT_DEPARTMENT_ID
    fake_department1.save()

    def cleanup():
        fake_department1.delete_instance()

    yield fake_department1

    cleanup()


@pytest.fixture()
def fake_department_sales():
    fake_department2 = department.Department.create(name="Sales")
    fake_department2.id = SALES_DEPARTMENT_ID
    fake_department2.save()

    def cleanup():
        fake_department2.delete_instance()

    yield fake_department2

    cleanup()


@pytest.fixture()
def fake_department_support():
    fake_department3 = department.Department.create(name="Support")
    fake_department3.id = SUPPORT_DEPARTMENT_ID
    fake_department3.save()

    def cleanup():
        fake_department3.delete_instance()

    yield fake_department3

    cleanup()


@pytest.fixture()
def fake_company():
    fake_company = company.Company.create(name="Total")

    def cleanup():
        fake_company.delete_instance()

    yield fake_company

    cleanup()


@pytest.fixture()
def fake_company2():
    fake_company = company.Company.create(name="Danone")

    def cleanup():
        fake_company.delete_instance()

    yield fake_company

    cleanup()


@pytest.fixture()
def fake_collaborator_management():
    fake_collaborator = collaborator.Collaborator.create(
        first_name="Fake",
        name="Manager",
        email="test@management.fr",
        password="testpass",
        department=MANAGEMENT_DEPARTMENT_ID,
    )

    def cleanup():
        fake_collaborator.delete_instance()

    yield fake_collaborator

    cleanup()


@pytest.fixture()
def fake_collaborator_sales():
    fake_collaborator = collaborator.Collaborator.create(
        first_name="Fake",
        name="Salesman",
        email="test@sales.fr",
        password="testpass",
        department=SALES_DEPARTMENT_ID,
    )

    def cleanup():
        fake_collaborator.delete_instance()

    yield fake_collaborator

    cleanup()


@pytest.fixture()
def fake_collaborator_sales2():
    fake_collaborator = collaborator.Collaborator.create(
        first_name="Plankton",
        name="Salesman",
        email="plankton@sales.fr",
        password="testpass",
        department=SALES_DEPARTMENT_ID,
    )

    def cleanup():
        fake_collaborator.delete_instance()

    yield fake_collaborator

    cleanup()


@pytest.fixture()
def fake_collaborator_support():
    fake_collaborator = collaborator.Collaborator.create(
        first_name="Fake",
        name="Support",
        email="test@support.fr",
        password="testpass",
        department=SUPPORT_DEPARTMENT_ID,
    )

    def cleanup():
        fake_collaborator.delete_instance()

    yield fake_collaborator

    cleanup()


@pytest.fixture()
def fake_collaborator_support2():
    fake_collaborator = collaborator.Collaborator.create(
        first_name="Gargamel",
        name="Support",
        email="gargamel@support.fr",
        password="testgargamel",
        department=SUPPORT_DEPARTMENT_ID,
    )

    def cleanup():
        fake_collaborator.delete_instance()

    yield fake_collaborator

    cleanup()


@pytest.fixture()
def fake_client(fake_company, fake_collaborator_sales):
    fake_client = client.Client.create(
        first_name="Gérard",
        name="Hermite",
        email="gerard@lamer.fr",
        phone="0655698748",
        company=fake_company.id,
        collaborator=fake_collaborator_sales.id,
    )

    def cleanup():
        fake_client.delete_instance()

    yield fake_client

    cleanup()


@pytest.fixture()
def fake_contract(fake_client, fake_collaborator_sales):
    fake_contract = contract.Contract.create(
        client=fake_client.id,
        collaborator=fake_collaborator_sales.id,
        total_sum=15000,
        signed=True,
    )

    def cleanup():
        fake_contract.delete_instance()

    yield fake_contract

    cleanup()


@pytest.fixture()
def fake_contract2(fake_client, fake_collaborator_sales):
    fake_contract = contract.Contract.create(
        client=fake_client.id,
        collaborator=fake_collaborator_sales.id,
        total_sum=12000,
        amount_due=10000,
        signed=True,
    )

    def cleanup():
        fake_contract.delete_instance()

    yield fake_contract

    cleanup()


@pytest.fixture()
def fake_contract3(fake_client, fake_collaborator_sales):
    fake_contract = contract.Contract.create(
        client=fake_client.id,
        collaborator=fake_collaborator_sales.id,
        total_sum=24000,
        amount_due=0,
        signed=True,
    )

    def cleanup():
        fake_contract.delete_instance()

    yield fake_contract

    cleanup()


@pytest.fixture()
def fake_contract_unsigned(fake_client, fake_collaborator_sales):
    fake_contract = contract.Contract.create(
        client=fake_client.id,
        collaborator=fake_collaborator_sales.id,
        total_sum=3200,
        amount_due=3200,
    )

    def cleanup():
        fake_contract.delete_instance()

    yield fake_contract

    cleanup()


@pytest.fixture()
def fake_event(fake_contract, fake_collaborator_support):
    fake_event = event.Event.create(
        contract=fake_contract,
        start_date="2024-09-10 14:00",
        end_date="2024-09-10 23:00",
        location="55, rue des Acacias - 77093 VILLEFANTOME",
        attendees=8,
        support=fake_collaborator_support.id,
    )

    def cleanup():
        fake_event.delete_instance()

    yield fake_event

    cleanup()


@pytest.fixture()
def fake_event2(fake_contract, fake_collaborator_support):
    fake_event = event.Event.create(
        contract=fake_contract,
        start_date="2024-09-10 14:00",
        end_date="2024-09-10 23:00",
        location="MARSEILLE",
        attendees=8,
        support=fake_collaborator_support.id,
    )

    def cleanup():
        fake_event.delete_instance()

    yield fake_event

    cleanup()


@pytest.fixture()
def fake_event_no_support(fake_contract):
    fake_event = event.Event.create(
        contract=fake_contract,
        start_date="2024-03-25 08:00",
        end_date="2024-03-25 12:00",
        location="3, rue de Paris - 75000 PARIS",
        attendees=15,
        support=None,
    )

    def cleanup():
        fake_event.delete_instance()

    yield fake_event

    cleanup()


@pytest.fixture()
def fake_event_no_support_2(fake_contract):
    fake_event = event.Event.create(
        contract=fake_contract,
        start_date="2024-03-25 08:00",
        end_date="2024-03-25 12:00",
        location="23, av des Champs Elysées - 75008 PARIS",
        attendees=15,
        support=None,
    )

    def cleanup():
        fake_event.delete_instance()

    yield fake_event

    cleanup()


@pytest.fixture()
def valid_token():
    payload = {
        "collaborator_id": 1,
        "email": "test@collab.fr",
        "department_id": 1,
        "exp": datetime.utcnow() + timedelta(hours=1),
    }

    fake_token = jwt.encode(payload, key=SECRET_KEY, algorithm="HS256")

    yield fake_token


@pytest.fixture()
def expired_token():
    payload = {
        "collaborator_id": 1,
        "email": "test@collab.fr",
        "department_id": 1,
        "exp": datetime.utcnow() - timedelta(hours=1),
    }

    fake_token = jwt.encode(payload, key=SECRET_KEY, algorithm="HS256")

    yield fake_token


@pytest.fixture()
def wrong_token():
    payload = {
        "collaborator_id": None,
        "email": "test@collab.fr",
        "department_id": 1,
        "exp": datetime.utcnow() + timedelta(hours=1),
    }

    fake_token = jwt.encode(payload, key=SECRET_KEY, algorithm="HS256")

    yield fake_token


@pytest.fixture()
def wrong_token_str():
    payload = {
        "collaborator_id": "Wrong",
        "email": "test@collab.fr",
        "department_id": 1,
        "exp": datetime.utcnow() + timedelta(hours=1),
    }

    fake_token = jwt.encode(payload, key=SECRET_KEY, algorithm="HS256")

    yield fake_token


@pytest.fixture()
def wrong_department_token():
    payload = {
        "collaborator_id": 1,
        "email": "test@collab.fr",
        "department_id": "2",
        "exp": datetime.utcnow() + timedelta(hours=1),
    }

    fake_token = jwt.encode(payload, key=SECRET_KEY, algorithm="HS256")

    yield fake_token


@pytest.fixture()
def monkey_dotenv(monkeypatch):
    dotenv_file = load_dotenv("test.env")

    monkeypatch.setattr(clicollaborator, "dotenv_file", dotenv_file)

    return dotenv_file


@pytest.fixture()
def monkey_token_check_management(monkeypatch):
    def return_monkey_token():
        return (
            True,
            {
                "collaborator_id": 1,
                "email": "etoile@mer.fr",
                "department_id": MANAGEMENT_DEPARTMENT_ID,
            },
        )

    monkeypatch.setattr(clicollaborator, "_verify_token", return_monkey_token)


@pytest.fixture()
def monkey_token_check_correct_sales(monkeypatch, fake_collaborator_sales):
    def return_monkey_token():
        return (
            True,
            {
                "collaborator_id": fake_collaborator_sales.id,
                "email": "etoile@mer.fr",
                "department_id": SALES_DEPARTMENT_ID,
            },
        )

    monkeypatch.setattr(clicollaborator, "_verify_token", return_monkey_token)


@pytest.fixture()
def monkey_token_check_correct_sales_plankton(monkeypatch, fake_collaborator_sales2):
    def return_monkey_token():
        return (
            True,
            {
                "collaborator_id": fake_collaborator_sales2.id,
                "email": fake_collaborator_sales2.email,
                "department_id": SALES_DEPARTMENT_ID,
            },
        )

    monkeypatch.setattr(clicollaborator, "_verify_token", return_monkey_token)


@pytest.fixture()
def monkey_token_check_fake_sales(monkeypatch):
    def return_monkey_token():
        return (
            True,
            {
                "collaborator_id": 50,
                "email": "etoile@mer.fr",
                "department_id": SALES_DEPARTMENT_ID,
            },
        )

    monkeypatch.setattr(clicollaborator, "_verify_token", return_monkey_token)


@pytest.fixture()
def monkey_token_check_support(monkeypatch, fake_event):
    def return_monkey_token():
        return (
            True,
            {
                "collaborator_id": fake_event.support.id,
                "email": "etoile@mer.fr",
                "department_id": SUPPORT_DEPARTMENT_ID,
            },
        )

    monkeypatch.setattr(clicollaborator, "_verify_token", return_monkey_token)


@pytest.fixture()
def monkey_token_check_support_gargamel(monkeypatch, fake_collaborator_support2):
    def return_monkey_token():
        return (
            True,
            {
                "collaborator_id": fake_collaborator_support2.id,
                "email": fake_collaborator_support2.email,
                "department_id": SUPPORT_DEPARTMENT_ID,
            },
        )

    monkeypatch.setattr(clicollaborator, "_verify_token", return_monkey_token)


@pytest.fixture()
def monkey_token_check_false(monkeypatch):
    def return_monkey_token():
        return False

    monkeypatch.setattr(clicollaborator, "_verify_token", return_monkey_token)


@pytest.fixture()
def monkey_read_token_correct(monkeypatch, valid_token):
    def return_monkey_read_token():
        return valid_token

    monkeypatch.setattr(clicollaborator, "_read_token", return_monkey_read_token)


@pytest.fixture()
def monkey_read_token_wrong(monkeypatch, wrong_token):
    def return_monkey_read_token():
        return wrong_token

    monkeypatch.setattr(clicollaborator, "_read_token", return_monkey_read_token)


@pytest.fixture()
def monkey_read_token_wrong_str(monkeypatch, wrong_token_str):
    def return_monkey_read_token():
        return wrong_token_str

    monkeypatch.setattr(clicollaborator, "_read_token", return_monkey_read_token)


@pytest.fixture()
def monkey_read_token_expired(monkeypatch, expired_token):
    def return_monkey_read_token():
        return expired_token

    monkeypatch.setattr(clicollaborator, "_read_token", return_monkey_read_token)


@pytest.fixture()
def monkey_read_token_wrong_department(monkeypatch, wrong_department_token):
    def return_monkey_read_token():
        return wrong_department_token

    monkeypatch.setattr(clicollaborator, "_read_token", return_monkey_read_token)


@pytest.fixture()
def monkey_capture_message_collaborator(monkeypatch):
    def return_monkey(*args, **kwargs):
        pass

    monkeypatch.setattr(clicollaborator.sentry_sdk, "capture_message", return_monkey)


@pytest.fixture()
def monkey_capture_message_contract(monkeypatch):
    def return_monkey(*args, **kwargs):
        pass

    monkeypatch.setattr(clicontract.sentry_sdk, "capture_message", return_monkey)
