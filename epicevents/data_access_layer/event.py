from peewee import *
from .database import BaseModel
from .contract import Contract
from .collaborator import Collaborator


class Event(BaseModel):
    contract = ForeignKeyField(Contract, backref="contract")
    start_date = DateField()
    end_date = DateField()
    location = CharField(max_length=150)
    attendees = IntegerField()
    notes = TextField(null=True)
    support = ForeignKeyField(Collaborator, backref="associated_support")
    
    # def save(self, *args, **kwargs):

    #     super().save(*args, **kwargs)