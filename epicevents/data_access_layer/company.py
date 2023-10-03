from peewee import *
from .database import BaseModel

class Company(BaseModel):
    name = CharField(max_length=50, unique=True)
    
