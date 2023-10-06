import re
from peewee import *
from datetime import date, datetime
from .database import BaseModel
from .contract import Contract
from .collaborator import Collaborator


class Event(BaseModel):
    contract = ForeignKeyField(Contract, backref="contract")
    start_date = DateTimeField()
    end_date = DateTimeField()
    location = CharField(max_length=150)
    attendees = IntegerField()
    notes = TextField(null=True)
    support = ForeignKeyField(Collaborator, backref="associated_support")
    
    def save(self, *args, **kwargs):
        if not self.contract and self.start_date and self.end_date and self.location:
            raise ValueError("Erreur : Veuillez renseigner les détails de l'évènement.")
        
        if not isinstance(self.contract.id, int):
            raise ValueError("Erreur : Veuillez entrer un identifiant de contrat valide.")
        
        if not isinstance(self.support.id, int):
            raise ValueError("Erreur : Veuillez entrer un identifiant de collaborateur valide.")
        
        self._validate_date()
        
        super().save(*args, **kwargs)


    def _validate_date(self):
        pattern = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$'
        if self.start_date and self.end_date:
            if not re.match(pattern, str(self.creation_date)):
                raise ValueError("Erreur : Veuillez entrer une date et une heure valides (Exemple : 2023-02-05 20:30)")
        else:
            raise ValueError("Erreur : Vous n'avez pas fourni de date de début. Veuillez entrer une date et une heure valides (Exemple : 2023-02-05 20:30)")