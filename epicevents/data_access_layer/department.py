from peewee import *
from epicevents.data_access_layer.database import BaseModel


class Department(BaseModel):
    name = CharField(max_length=50, unique=True)
    
