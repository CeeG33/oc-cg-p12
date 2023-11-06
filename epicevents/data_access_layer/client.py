import re
from datetime import datetime
from peewee import *
from .database import BaseModel
from .company import Company
from .collaborator import Collaborator


class Client(BaseModel):
    """Represents a client in the CRM system."""

    first_name = CharField(max_length=25)
    name = CharField(max_length=25)
    email = CharField(max_length=50, unique=True, null=True)
    phone = CharField(max_length=20, unique=True)
    company = ForeignKeyField(Company, backref="company")
    creation_date = DateTimeField(default=datetime.now().date)
    last_update = DateTimeField(null=True)
    collaborator = ForeignKeyField(
        Collaborator, backref="associated_sales", on_delete="SET NULL"
    )

    def save(self, *args, **kwargs):
        """
        Saves the client's information with validation checks.

        Raises:
            ValueError: If required fields are missing or validation checks fail.
        """
        if not (self.first_name and self.name):
            raise ValueError(
                "Erreur : Vous n'avez pas renseigné les détails du client."
            )
        if not isinstance(self.collaborator, Collaborator):
            raise ValueError(
                "Erreur : Veuillez entrer un identifiant de collaborateur valide."
            )
        if not isinstance(self.company, Company):
            raise ValueError(
                "Erreur : Veuillez entrer un identifiant d'entreprise valide."
            )
        self._validate_name()
        self._validate_email()
        self._validate_date()
        self.first_name.capitalize()
        self.name.capitalize()
        super().save(*args, **kwargs)

    def _validate_name(self):
        """
        Validates the first name and last name.

        Raises:
            ValueError: If the first name or last name format is incorrect.
        """
        pattern = r"^[a-zA-ZÀ-ÿ-]+$"
        if not re.match(pattern, self.first_name):
            raise ValueError(
                "Erreur : Veuillez entrer un prénom correct (Exemple : Alain)"
            )

        if not re.match(pattern, self.name):
            raise ValueError(
                "Erreur : Veuillez entrer un nom de famille correct (Exemple : Terieur)"
            )

    def _validate_email(self):
        """
        Validates the email address.

        Raises:
            ValueError: If the email format is incorrect.
        """
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, self.email):
            raise ValueError(
                "Erreur : Veuillez entrer un email valide (Exemple : alain.terieur@epicevents.com)"
            )

    def _validate_date(self):
        """
        Validates date fields.

        Raises:
            ValueError: If the date format is incorrect.
        """
        pattern = r"^\d{4}-\d{2}-\d{2}$"
        pattern2 = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$"
        if not (
            re.match(pattern, str(self.creation_date))
            or re.match(pattern2, str(self.creation_date))
        ):
            raise ValueError(
                "Erreur : Veuillez entrer une date valide (Exemple : 2023-05-23)"
            )

        if self.last_update:
            if not (
                re.match(pattern, str(self.last_update))
                or re.match(pattern2, str(self.last_update))
            ):
                raise ValueError(
                    "Erreur : Veuillez entrer une date valide (Exemple : 2023-05-23)"
                )
