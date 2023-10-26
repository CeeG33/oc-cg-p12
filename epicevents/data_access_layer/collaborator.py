import re
from datetime import datetime, timedelta, timezone
from peewee import *
from argon2 import PasswordHasher
from .database import BaseModel
from .department import Department

ph = PasswordHasher()


class Collaborator(BaseModel):
    """Represents a collaborator (user) in the CRM system."""

    first_name = CharField(max_length=25)
    name = CharField(max_length=25)
    email = CharField(max_length=50, unique=True)
    password = CharField()
    department = ForeignKeyField(Department, backref="department")

    def save(self, *args, **kwargs):
        """
        Saves the collaborator's information with validation checks.

        Raises:
            ValueError: If required fields are missing or validation checks fail.
        """
        if not self.__data__:
            raise ValueError(
                "Erreur : Vous n'avez pas renseigné les détails du collaborateur."
            )
        self._validate_name()
        self._validate_email()
        self.password = ph.hash(self.password)
        self.first_name.capitalize()
        self.name.upper()
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

    def get_data(self):
        """Returns a dictionnary with the collaborator's information."""
        collaborator_data = {
            "collaborator_id": f"{self.id}",
            "email": f"{self.email}",
            "department_id": f"{self.department.id}",
            "exp": datetime.now(tz=timezone.utc) + timedelta(hours=1),
        }

        return collaborator_data
