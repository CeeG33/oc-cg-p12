from .database import psql_db
from .client import Client
from .collaborator import Collaborator
from .company import Company
from .contract import Contract
from .department import Department
from .event import Event

"""Connecting to the database"""
psql_db.connect()

"""Table creation"""
psql_db.create_tables([Client, Collaborator, Company, Contract, Department, Event])

Collaborator.create(
    identity="Admin",
    email="admin@epicevents.com",
    password="admin",
    department=1
)

# Collaborator.delete_by_id(6)


"""Closing the database"""
psql_db.close()