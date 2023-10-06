import pytest
import os
from peewee import PostgresqlDatabase, SqliteDatabase
from dotenv import load_dotenv
from epicevents.data_access_layer import client, collaborator, company, contract, department, event
from epicevents.data_access_layer import database

MODELS = [client.Client,
          collaborator.Collaborator,
          company.Company,
          contract.Contract,
          department.Department,
          event.Event]

test_db = SqliteDatabase(":memory:")
test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
test_db.connect()
test_db.create_tables(MODELS)

@pytest.fixture(autouse=True)
def test_database(monkeypatch):
    mocked_database = monkeypatch.setattr(database, "psql_db", test_db)
    return mocked_database

@pytest.fixture()
def fake_department():
    fake_department = department.Department.create(name="Recherche")
    
    def cleanup():
        fake_department.delete_instance()
    
    yield fake_department
    
    cleanup()
    
@pytest.fixture()
def fake_company():
    fake_company = company.Company.create(name="Total")
    
    def cleanup():
        fake_company.delete_instance()
    
    yield fake_company
    
    cleanup()
    
@pytest.fixture()
def fake_collaborator():
    collaborator_department = department.Department.create(name="Développement")
    fake_collaborator = collaborator.Collaborator.create(identity="Fake Collaborator",
                                                         email="test@company.fr",
                                                         password="testpass",
                                                         department=collaborator_department)
    
    def cleanup():
        fake_collaborator.delete_instance()
        collaborator_department.delete_instance()
    
    yield fake_collaborator
    
    cleanup()