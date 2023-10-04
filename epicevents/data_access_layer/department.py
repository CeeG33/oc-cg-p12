import re
from peewee import *
from playhouse.migrate import migrate
from .database import BaseModel

class Department(BaseModel):
    name = CharField(max_length=50, unique=True)
    
    def save(self, *args, **kwargs):
        if not self.__data__:
            raise ValueError("Erreur : Vous n'avez pas renseigné le nom du département.")
        self._validate_name()
        self.name.capitalize()
        super().save(*args, **kwargs)
        
    def _validate_name(self):
        pattern = r'^[a-zA-ZÀ-ÿ]+$'
        try: 
            re.match(pattern, self.name)  
        except TypeError:
            raise ValueError("Erreur : Veuillez entrer un nom valide (Exemple : Ressources Humaines)")
