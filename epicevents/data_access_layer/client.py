import re
from datetime import date, datetime, timedelta
from peewee import *
from .database import BaseModel
from .company import Company
from .collaborator import Collaborator

def _get_date():
    return date.today()

class Client(BaseModel):
    identity = CharField(max_length=50, unique=True)
    email = CharField(max_length=50, unique=True, null=True)
    phone = CharField(max_length=20, unique=True)
    company = ForeignKeyField(Company, backref="company")
    creation_date = DateField()
    last_update = DateField(null=True)
    collaborator = ForeignKeyField(Collaborator, backref="associated_sales")
    
    def save(self, *args, **kwargs):
        if not self.identity:
            raise ValueError("Erreur : Vous n'avez pas renseigné les détails du client.")
        self._validate_identity()
        self._validate_email()
        self.identity.capitalize()
        super().save(*args, **kwargs)
        
    def _validate_identity(self):
        pattern = r'^[a-zA-ZÀ-ÿ-]+ [a-zA-ZÀ-ÿ-]+$'
        if not re.match(pattern, self.identity):
            raise ValueError("Erreur : Veuillez entrer une identité correcte (Exemple : Alain Terieur)")
        
    def _validate_email(self):
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(pattern, self.email):
            raise ValueError("Erreur : Veuillez entrer un email valide (Exemple : alain.terieur@epicevents.com)")
        
    # def get_data(self):
    #     client_data = {
    #         "client_id" : f"{self.id}",
    #         "email": f"{self.email}",
    #         "company_id": f"{self.company}",
    #         "collaborator_id": f"{self.collaborator}",
    #     }
    
    #     return client_data