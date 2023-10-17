import os, jwt, typer
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from dotenv import load_dotenv, find_dotenv, set_key
from epicevents.data_access_layer.collaborator import Collaborator

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
    os.environ["TOKEN"] = token

def _read_token():
    return os.environ["TOKEN"]

def _verify_token():
    try:
        decoded_payload = jwt.decode(_read_token(), key=SECRET_KEY, algorithms=["HS256"])
    except ExpiredSignatureError:
        raise ExpiredSignatureError("Token expiré, veuillez vous réauthentifier.")
    
    collaborator_id = decoded_payload.get("collaborator_id")
    
    if collaborator_id is None or not isinstance(int(collaborator_id), int):
        raise InvalidTokenError("Le token n'est pas valide, veuillez vous réauthentifier.")
    
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
                    typer.echo("La base de donnée ne contient aucun collaborateur.")
                
                typer.echo(f"[ID] : {user.id} -- [Prénom] : {user.first_name} -- [Nom] : {user.name} -- [Email] : {user.email} -- [Departement] : {user.department.name}")
        
        else:
            typer.echo("Action restreinte.")
    
    else:
        typer.echo("Veuillez vous authentifier et réessayer.")


@app.command()
def create(first_name: str, name: str, email: str, password: str, department: int):
    token_check = _verify_token()
    if token_check:
        collaborator_department = token_check[1]["department_id"]
        
        if int(collaborator_department) == MANAGEMENT_DEPARTMENT_ID:
            Collaborator.create(first_name=first_name, name=name, email=email, password=password, department=department)
            typer.echo(f"Le collaborateur {first_name} {name} a été créé avec succès.")
        
        else:
            typer.echo("Action restreinte.")
        
    else:
        typer.echo("Veuillez vous authentifier et réessayer.")


## CONTINUER ICI
@app.command()
def update(collaborator_id: int):
    token_check = _verify_token()
    if token_check:
        collaborator_department = token_check[1]["department_id"]
        
        if int(collaborator_department) == MANAGEMENT_DEPARTMENT_ID:
            ## Ecrire la commande qui MAJ le collaborateur
            typer.echo(f"Le collaborateur {first_name} {name} a été mis à jour avec succès.")
        
        else:
            typer.echo("Action restreinte.")
        
    else:
        typer.echo("Veuillez vous authentifier et réessayer.")


## CONTINUER ICI
@app.command()
def delete(collaborator_id: int):
    token_check = _verify_token()
    if token_check:
        collaborator_department = token_check[1]["department_id"]
        
        if int(collaborator_department) == MANAGEMENT_DEPARTMENT_ID:
            ## Ecrire la commande qui supprime le collaborateur
            typer.echo(f"Le collaborateur {first_name} {name} a été supprimé avec succès.")
        
        else:
            typer.echo("Action restreinte.")
        
    else:
        typer.echo("Veuillez vous authentifier et réessayer.")


if __name__ == "__main__":
    app()