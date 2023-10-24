from data_access_layer.database import psql_db
from data_access_layer.client import Client
from data_access_layer.collaborator import Collaborator
from data_access_layer.company import Company
from data_access_layer.contract import Contract
from data_access_layer.department import Department
from data_access_layer.event import Event

"""Connecting to the database"""
psql_db.connect()

"""Table creation"""
psql_db.create_tables([Client, Collaborator, Company, Contract, Department, Event])

# Department.create(name="Management")
# Department.create(name="Sales")
# Department.create(name="Support")

Collaborator.create(
    first_name="Admin",
    name="Test",
    email="admin@epicevents.com",
    password="admin",
    department=1
)

# Collaborator.delete_by_id(6)


"""Closing the database"""
psql_db.close()