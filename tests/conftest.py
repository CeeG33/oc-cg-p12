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
    
@pytest.fixture()
def fake_client():
    collaborator_department = department.Department.create(name="Bâteau")
    client_company = company.Company.create(name="Thalès")
    salesman = collaborator.Collaborator.create(identity="Patrick Etoile",
                                                email="patrick@etoile.fr",
                                                password="etoile",
                                                department=collaborator_department)
    fake_client = client.Client.create(identity="Bernard Hermite",
                                       email="bernard@lamer.fr",
                                       phone="0654978959",
                                       company=client_company,
                                       collaborator=salesman)
    
    def cleanup():
        fake_client.delete_instance()
        collaborator_department.delete_instance()
        client_company.delete_instance()
        salesman.delete_instance()
    
    yield fake_client
    
    cleanup()
    

@pytest.fixture()
def fake_contract():
    collaborator_department = department.Department.create(name="Bâteau")
    client_company = company.Company.create(name="Thalès")
    salesman = collaborator.Collaborator.create(identity="Patrick Etoile",
                                                email="patrick@etoile.fr",
                                                password="etoile",
                                                department=collaborator_department)
    fake_client = client.Client.create(identity="Bernard Hermite",
                                       email="bernard@lamer.fr",
                                       phone="0654978959",
                                       company=client_company,
                                       collaborator=salesman)
    fake_contract = contract.Contract.create(client=fake_client,
                                             collaborator=fake_collaborator,
                                             total_sum="15000")
    
    def cleanup():
        fake_contract.delete_instance()
        fake_client.delete_instance()
        collaborator_department.delete_instance()
        client_company.delete_instance()
        salesman.delete_instance()
    
    yield fake_contract
    
    cleanup()