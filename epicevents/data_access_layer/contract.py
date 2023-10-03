from datetime import date
from peewee import *
from .database import BaseModel
from .client import Client
from .collaborator import Collaborator
from .department import Department


class Contract(BaseModel):
    client = ForeignKeyField(Client, backref="client")
    collaborator = ForeignKeyField(Collaborator, backref="associated_sales")
    total_sum = FloatField()
    amount_due = FloatField(null=True)
    creation_date = DateField(default=date.today())
    signed = BooleanField(default=False)
    
    # def save(self, *args, **kwargs):

    #     super().save(*args, **kwargs)