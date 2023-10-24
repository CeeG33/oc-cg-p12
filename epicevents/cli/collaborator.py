import os, jwt, typer
from typing import Optional
from typing_extensions import Annotated
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from peewee import DoesNotExist
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from dotenv import load_dotenv, find_dotenv, set_key
from epicevents.sentry import sentry_sdk
from epicevents.data_access_layer.collaborator import Collaborator
from epicevents.data_access_layer.department import Department

dotenv_file = load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
if os.getenv("TOKEN"):
    TOKEN = os.getenv("TOKEN")

MANAGEMENT_DEPARTMENT_ID = 1
SALES_DEPARTMENT_ID = 2
SUPPORT_DEPARTMENT_ID = 3

app = typer.Typer()

ph = PasswordHasher()

def _generate_token(collaborator):
    token = jwt.encode(collaborator.get_data(), key=SECRET_KEY, algorithm="HS256")
    return token

def _memorize_token(token):
    set_key(".env", "TOKEN", token)

def _read_token():
    return os.environ["TOKEN"]

def _verify_token():
    try:
        decoded_payload = jwt.decode(_read_token(), key=SECRET_KEY, algorithms=["HS256"])
    except ExpiredSignatureError:
        print("Token expiré, veuillez vous réauthentifier.")
        raise ExpiredSignatureError
    
    collaborator_id = decoded_payload.get("collaborator_id")
    
    if collaborator_id is None or not isinstance(int(collaborator_id), int):
        print("Le token n'est pas valide, veuillez vous réauthentifier.")
        raise InvalidTokenError
    
    return True, decoded_payload


@app.command()
def login(email: str, password: str):
    collaborator = Collaborator.get_or_none(Collaborator.email == email)
    
    if collaborator:
        if hasattr(collaborator, "password"):
            try:
                password_check = ph.verify(collaborator.password, password)
            except VerifyMismatchError:
                typer.echo("Nom d'utilisateur ou mot de passe incorrect.")
                raise typer.Exit(code=1)
        
    if not collaborator:
        typer.echo("Nom d'utilisateur ou mot de passe incorrect.")
        raise typer.Exit(code=1)
        
    typer.echo("Authentification réussie.")
    token = _generate_token(collaborator)
    _memorize_token(token)


@app.command()
def list():
    token_check = _verify_token()

    if token_check:
        collaborator_department = token_check[1]["department_id"]
        
        if int(collaborator_department) == MANAGEMENT_DEPARTMENT_ID:
            queryset = Collaborator.select() 
            
            for user in queryset:
                if len(Collaborator) == 0:
                    print("La base de donnée ne contient aucun collaborateur.")
                    raise typer.Exit()
                
                print(f"[ID] : {user.id} -- [Prénom] : {user.first_name} -- [Nom] : {user.name} -- [Email] : {user.email} -- [Departement] : {user.department.name}")
        
        else:
            print("Action restreinte.")
            raise typer.Exit()
    
    else:
        print("Veuillez vous authentifier et réessayer.")
        raise typer.Exit()


@app.command()
def create(first_name: str, name: str, email: str, password: str, department: int):
    token_check = _verify_token()
    if token_check:
        collaborator_department = token_check[1]["department_id"]
        collaborator_id = token_check[1]["collaborator_id"]
        
        if int(collaborator_department) == MANAGEMENT_DEPARTMENT_ID:
            Collaborator.create(first_name=first_name, name=name, email=email, password=password, department=department)
            print(f"Le collaborateur {first_name} {name} a été créé avec succès.")
            sentry_sdk.capture_message(f"[CREATION COLLABORATEUR PAR COLLABORATEUR N°{collaborator_id}] >> Prénom : {first_name} - Nom : {name} - Email : {email} - Département : {department}")
        
        else:
            print("Action restreinte.")
            raise typer.Exit()
        
    else:
        print("Veuillez vous authentifier et réessayer.")
        raise typer.Exit()


@app.command()
def update(collaborator_id: Annotated[int, typer.Argument()],
           new_value: Annotated[str, typer.Argument()], 
           first_name: Annotated[bool, typer.Option()] = False,
           name: Annotated[bool, typer.Option()] = False,
           email: Annotated[bool, typer.Option()] = False,
           password: Annotated[bool, typer.Option()] = False,
           department: Annotated[bool, typer.Option()] = False
        ):
    token_check = _verify_token()
    if token_check:
        collaborator_department = token_check[1]["department_id"]
        user_id = token_check[1]["collaborator_id"]
        
        if int(collaborator_department) == MANAGEMENT_DEPARTMENT_ID:
            try:
                collaborator = Collaborator.get(Collaborator.id == collaborator_id)
                
                if first_name:
                    collaborator.first_name = new_value
                    collaborator.save()
                    print(f"Le champ 'Prénom' du collaborateur n°{collaborator_id} a été mis à jour avec succès.")
                    sentry_sdk.capture_message(f"[MAJ COLLABORATEUR N°{collaborator_id} PAR COLLABORATEUR N°{user_id}] >> Prénom : {new_value}")
                    
                elif name:
                    collaborator.name = new_value
                    collaborator.save()
                    print(f"Le champ 'Nom' du collaborateur n°{collaborator_id} a été mis à jour avec succès.")
                    sentry_sdk.capture_message(f"[MAJ COLLABORATEUR N°{collaborator_id} PAR COLLABORATEUR N°{user_id}] >> Nom : {new_value}")
                    
                elif email:
                    collaborator.email = new_value
                    collaborator.save()
                    print(f"Le champ 'Email' du collaborateur n°{collaborator_id} a été mis à jour avec succès.")
                    sentry_sdk.capture_message(f"[MAJ COLLABORATEUR N°{collaborator_id} PAR COLLABORATEUR N°{user_id}] >> Email : {new_value}")
                    
                elif password:
                    collaborator.password = new_value
                    collaborator.save()
                    print(f"Le champ 'Mot de passe' du collaborateur n°{collaborator_id} a été mis à jour avec succès.")
                    sentry_sdk.capture_message(f"[MAJ COLLABORATEUR N°{collaborator_id} PAR COLLABORATEUR N°{user_id}] >> Nouveau mot de passe")
                    
                elif department:
                    department_check = Department.get_or_none(Department.id == new_value)
                    
                    if department_check:
                        collaborator.department = new_value
                        collaborator.save()
                        print(f"Le champ 'Département' du collaborateur n°{collaborator_id} a été mis à jour avec succès.")
                        sentry_sdk.capture_message(f"[MAJ COLLABORATEUR N°{collaborator_id} PAR COLLABORATEUR N°{user_id}] >> Département : {new_value}")
                    
                    else:
                        print("Veuillez entrer un numéro de département valide.")
                        raise typer.Exit(code=1)
                    
                else:
                    print("Vous n'avez pas sélectionné d'attribut à modifier.")
                    raise typer.Exit()
            
            except DoesNotExist:
                print(f"Aucun collaborateur trouvé avec l'ID n°{collaborator_id}.")

        else:
            print("Action restreinte.")
            raise typer.Exit()
        
    else:
        print("Veuillez vous authentifier et réessayer.")
        raise typer.Exit()


@app.command()
def delete(collaborator_id: int):
    token_check = _verify_token()
    if token_check:
        collaborator_department = token_check[1]["department_id"]
        user_id = token_check[1]["collaborator_id"]
        
        if int(collaborator_department) == MANAGEMENT_DEPARTMENT_ID:
            try:
                collaborator = Collaborator.get(Collaborator.id == collaborator_id)
                collaborator.delete_instance()
                print(f"Le collaborateur n°{collaborator_id} a été supprimé avec succès.")
                sentry_sdk.capture_message(f"[SUPPRESSION COLLABORATEUR N°{collaborator_id} PAR COLLABORATEUR N°{user_id}]")
            
            except DoesNotExist:
                print(f"Aucun collaborateur trouvé avec l'ID n°{collaborator_id}.")

        else:
            print("Action restreinte.")
            raise typer.Exit()
        
    else:
        print("Veuillez vous authentifier et réessayer.")
        raise typer.Exit()


if __name__ == "__main__":
    app()