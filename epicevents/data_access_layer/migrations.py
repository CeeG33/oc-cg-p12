from database import psql_db
from department import Department
from collaborator import Collaborator

"""Connecting to the database"""
psql_db.connect()

"""Table creation"""
psql_db.create_tables([Department, Collaborator])

# Collaborator.create(
#     identity="Ciran GÜRBÜZ",
#     email="ciran@epicevents.com",
#     password="Ceegee",
#     department=1
# )

# Collaborator.delete_by_id(6)


"""Closing the database"""
psql_db.close()