import os, jwt, typer
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from argon2 import PasswordHasher
from dotenv import load_dotenv, find_dotenv, set_key
from epicevents.data_access_layer.collaborator import Collaborator

dotenv_file = load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
if os.getenv("TOKEN"):
    TOKEN = os.getenv("TOKEN")

MANAGEMENT_DEPARTMENT_ID = 1

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
    collaborator = Collaborator.get_or_none(email=email)
    password_check = ph.verify(collaborator.password, password)
    
    if not collaborator:
        typer.echo("Nom d'utilisateur ou mot de passe incorrect.")
    
    if not password_check:
        typer.echo("Nom d'utilisateur ou mot de passe incorrect.")
        
    typer.echo("Authentification réussie.")
    token = _generate_token(collaborator)
    _memorize_token(token)


@app.command()
def show_all_collaborators():
    token_check = _verify_token()
    if token_check:
        collaborator_department = token_check.get("department_id")
        
        if collaborator_department == MANAGEMENT_DEPARTMENT_ID:
            queryset = Collaborator.select()
            
            for user in queryset:
                if queryset.len() == 0:
                    typer.echo("La base de donnée ne contient aucun collaborateur.")
                
                typer.echo(f"[ID] : {user.id} -- [Identité] : {user.identity} -- [Email] : {user.email} -- [Departement] : {user.department.name}")
        
        typer.echo("Action restreinte.")
    
    typer.echo("Veuillez vous authentifier.")


@app.command()
def create_collaborator(identity: str, email: str, password: str, department: int):
    token_check = _verify_token()
    if token_check:
        collaborator_department = token_check.get("department_id")
        
        if collaborator_department == MANAGEMENT_DEPARTMENT_ID:
            Collaborator.create(identity=identity, email=email, password=password, department=department)
            typer.echo(f"Le collaborateur {identity} a été créé avec succès.")

        typer.echo("Action restreinte.")
        
    typer.echo("Veuillez vous authentifier.")


if __name__ == "__main__":
    app()