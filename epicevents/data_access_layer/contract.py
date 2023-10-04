from datetime import date
from peewee import *
from babel.numbers import format_currency
from .database import BaseModel
from .client import Client
from .collaborator import Collaborator
from .department import Department

def _get_date():
    return date.today()

class Contract(BaseModel):
    client = ForeignKeyField(Client, backref="client")
    collaborator = ForeignKeyField(Collaborator, backref="associated_sales")
    total_sum = FloatField()
    amount_due = FloatField(null=True)
    creation_date = DateField(default=_get_date())
    signed = BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.client:
            raise ValueError("Erreur : Vous n'avez pas renseigné les détails du client.")
        
        self._format_number(self.total_sum)
        
        if self.amount_due:
            self._format_number(self.amount_due)
        
        self.creation_date = self._default_date()
        
        super().save(*args, **kwargs)
        
    def _format_number(self, amount):
        amount = format_currency(amount, "EUR", locale="fr_FR")
        