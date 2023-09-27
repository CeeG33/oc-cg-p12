import os
from dotenv import load_dotenv
from peewee import *

load_dotenv()
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

psql_db = PostgresqlDatabase(DB_NAME, user=DB_USER, password=DB_PASSWORD)

class BaseModel(Model):
    class Meta:
        database = psql_db