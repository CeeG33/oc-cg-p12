from peewee import *
from playhouse.migrate import migrate
from .database import BaseModel

class Department(BaseModel):
    name = CharField(max_length=50, unique=True)
    
