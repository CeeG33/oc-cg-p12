from datetime import date
from peewee import *
from database import BaseModel
from company import Company
from collaborator import Collaborator


class Client(BaseModel):
    identity = CharField(max_length=50, unique=True)
    email = CharField(max_length=50, unique=True, null=True)
    phone = CharField(max_length=20, unique=True)
    company = ForeignKeyField(Company, backref="company")
    creation_date = DateField(default=date.today())
    last_update = DateField()
    collaborator = ForeignKeyField(Collaborator, backref="associated_sales")
    
    # def save(self, *args, **kwargs):

    #     super().save(*args, **kwargs)