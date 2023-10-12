import re
from datetime import datetime, timedelta
from peewee import *
from argon2 import PasswordHasher
from .database import BaseModel
from .department import Department

ph = PasswordHasher()
class Collaborator(BaseModel):
    identity = CharField(max_length=50, unique=True)
    email = CharField(max_length=50, unique=True)
    password = CharField()
    department = ForeignKeyField(Department, backref="department")
    
    def save(self, *args, **kwargs):
        if not self.__data__:
            raise ValueError("Erreur : Vous n'avez pas renseigné les détails du collaborateur.")
        self._validate_identity()
        self._validate_email()
        self.password = ph.hash(self.password)
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
        
    def get_data(self):
        collaborator_data = {
            "collaborator_id" : f"{self.id}",
            "email": f"{self.email}",
            "department_id": f"{self.department}",
            "exp": datetime.utcnow() + timedelta(hours=1)
        }
    
        return collaborator_data