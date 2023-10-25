from dotenv import get_key
from data_access_layer.database import psql_db
from data_access_layer.client import Client
from data_access_layer.collaborator import Collaborator
from data_access_layer.company import Company
from data_access_layer.contract import Contract
from data_access_layer.department import Department
from data_access_layer.event import Event

ADMIN_EMAIL = get_key(".env", "ADMIN_EMAIL")
ADMIN_PASSWORD = get_key(".env", "ADMIN_PASSWORD")


"""Connecting to the database."""
psql_db.connect()


"""Table creation."""
psql_db.create_tables([Client, Collaborator, Company, Contract, Department, Event])


"""Creating EpicEvents' departments."""
Department.create(name="Management")
Department.create(name="Sales")
Department.create(name="Support")


"""Creating fake companies."""
Company.create(name="L'Oréal")
Company.create(name="Ubisoft")
Company.create(name="Riot Games")


"""Creating the admin user."""
Collaborator.create(
    first_name="Admin",
    name="Test",
    email=ADMIN_EMAIL,
    password=ADMIN_PASSWORD,
    department=1,
)


"""Closing the database."""
psql_db.close()
