import re
from peewee import *
from .database import BaseModel
from .contract import Contract
from .collaborator import Collaborator


class Event(BaseModel):
    """Represents an event in the CRM system."""

    contract = ForeignKeyField(Contract, backref="contract")
    start_date = DateTimeField()
    end_date = DateTimeField()
    location = CharField(max_length=150)
    attendees = IntegerField()
    notes = TextField(null=True)
    support = ForeignKeyField(
        Collaborator, backref="associated_support", on_delete="SET NULL", null=True
    )

    def save(self, *args, **kwargs):
        """
        Saves the event's information with validation checks.

        Raises:
            ValueError: If required fields are missing or validation checks fail.
        """
        if not (self.contract and self.start_date and self.end_date and self.location):
            raise ValueError("Erreur : Veuillez renseigner les détails de l'évènement.")

        if not isinstance(self.contract, Contract):
            raise ValueError(
                "Erreur : Veuillez entrer un identifiant de contrat valide."
            )

        if self.support is not None and not isinstance(self.support, Collaborator):
            raise ValueError(
                "Erreur : Veuillez entrer un identifiant de collaborateur valide."
            )

        if not str(self.attendees).isdigit() or int(self.attendees) <= 1:
            raise ValueError(
                "Erreur : Veuillez entrer un nombre de participant supérieur à 1."
            )

        self._validate_date()

        super().save(*args, **kwargs)

    def _validate_date(self):
        """
        Validates the date.

        Raises:
            ValueError: If the date format is incorrect.
        """
        pattern = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$"
        pattern2 = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$"

        if not (
            (
                (re.match(pattern, str(self.start_date)))
                or (re.match(pattern2, str(self.start_date)))
            )
            and (
                (re.match(pattern, str(self.end_date)))
                or (re.match(pattern2, str(self.end_date)))
            )
        ):
            raise ValueError(
                "Erreur : Veuillez entrer une date et une heure valides (Exemple : 2023-02-05 20:30)"
            )
