from peewee import *
from argon2 import PasswordHasher
from database import BaseModel
from department import Department

ph = PasswordHasher()
class Collaborator(BaseModel):
    identity = CharField(max_length=50, unique=True)
    email = CharField(max_length=50, unique=True)
    password = CharField()
    department = ForeignKeyField(Department, backref="department")
    
    def save(self, *args, **kwargs):
        self.password = ph.hash(self.password)
        self.identity.capitalize()
        super().save(*args, **kwargs)