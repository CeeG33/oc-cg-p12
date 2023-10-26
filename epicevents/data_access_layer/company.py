import re
from peewee import *
from .database import BaseModel


class Company(BaseModel):
    """Represents a company in the CRM system."""

    name = CharField(max_length=50, unique=True)

    def save(self, *args, **kwargs):
        """
        Saves the company's information with validation checks.

        Raises:
            ValueError: If required fields are missing or validation checks fail.
        """
        if not self.__data__:
            raise ValueError(
                "Erreur : Vous n'avez pas renseigné le nom de l'entreprise."
            )
        self._validate_name()
        self.name.capitalize()
        super().save(*args, **kwargs)

    def _validate_name(self):
        """
        Validates the name.

        Raises:
            ValueError: If the name format is incorrect.
        """
        pattern = r"^[a-zA-ZÀ-ÿ0-9_.+-]+$"
        try:
            re.match(pattern, self.name)
        except TypeError:
            raise ValueError(
                "Erreur : Veuillez entrer un nom valide (Exemple : Epic Events)"
            )
