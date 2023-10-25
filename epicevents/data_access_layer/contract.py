import re
import datetime as dt
from datetime import date, datetime
from peewee import *
from .database import BaseModel
from .client import Client
from .collaborator import Collaborator
from .department import Department


class Contract(BaseModel):
    client = ForeignKeyField(Client, backref="client")
    collaborator = ForeignKeyField(
        Collaborator, backref="associated_sales", on_delete="SET NULL"
    )
    total_sum = FloatField()
    amount_due = FloatField(null=True)
    creation_date = DateTimeField(default=datetime.now().date)
    signed = BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.client:
            raise ValueError("Erreur : Veuillez renseigner les détails du contrat.")

        if not isinstance(self.collaborator.id, int):
            raise ValueError(
                "Erreur : Veuillez entrer un identifiant de collaborateur valide."
            )

        if not isinstance(self.client.id, int):
            raise ValueError("Erreur : Veuillez entrer un identifiant client valide.")

        if not isinstance(self.total_sum, (int, float)):
            raise ValueError("Erreur : Veuillez entrer un montant valide.")

        if self.amount_due != None and not isinstance(self.amount_due, (int, float)):
            raise ValueError("Erreur : Veuillez entrer un montant valide.")

        if self.signed not in ("True", "False", True, False):
            raise ValueError(
                "Erreur : Le champ signed doit être rempli avec True(= contrat signé) ou False(=contrat non signé)."
            )

        self._validate_date()

        super().save(*args, **kwargs)

    def _validate_date(self):
        pattern = r"^\d{4}-\d{2}-\d{2}$"
        pattern2 = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$"
        if not (
            re.match(pattern, str(self.creation_date))
            or re.match(pattern2, str(self.creation_date))
        ):
            raise ValueError(
                "Erreur : Veuillez entrer une date valide (Exemple : 2023-05-23)"
            )
