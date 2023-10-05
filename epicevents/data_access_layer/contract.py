from datetime import date, datetime
from peewee import *
from babel.numbers import format_currency
from .database import BaseModel
from .client import Client
from .collaborator import Collaborator
from .department import Department


class Contract(BaseModel):
    client = ForeignKeyField(Client, backref="client")
    collaborator = ForeignKeyField(Collaborator, backref="associated_sales")
    total_sum = FloatField()
    amount_due = FloatField(null=True)
    creation_date = DateField(default=datetime.now().date)
    signed = BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.client:
            raise ValueError("Erreur : Veuillez renseigner les détails du contrat.")
        
        if self.signed not in (True, False):
            raise ValueError("Erreur : Le champ signed doit être rempli avec True(= contrat signé) ou False(=contrat non signé).")
        
        super().save(*args, **kwargs)
        
        if self.total_sum:
            self.total_sum = self._format_number(self.total_sum)
        
        if self.amount_due:
            self.amount_due = self._format_number(self.amount_due)
        
    def _format_number(self, amount):
        amount = format_currency(amount, "EUR", locale="fr_FR")
        return amount
        