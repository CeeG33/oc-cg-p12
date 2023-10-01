import typer
from data_access_layer.collaborator import Collaborator
from data_access_layer.client import Client
from data_access_layer.contract import Contract
from data_access_layer.event import Event
from argon2 import PasswordHasher


app = typer.Typer()

ph = PasswordHasher()


@app.command()
def login(email: str, password: str):
    collaborator = Collaborator.get_or_none(email=email)
    password_check = ph.verify(collaborator.password, password)
    
    if not collaborator:
        typer.echo("Nom d'utilisateur incorrect.")
    
    if not password_check:
        typer.echo("Mot de passe incorrect.")
        
    typer.echo("Authentification réussie.")


@app.command()
def show_all_collaborators():
    if collaborator.department == 1: #Si collab fait parti du Management
        
        queryset = Collaborator.select()
        
        for user in queryset:
            if queryset.len() == 0:
                typer.echo("La base de donnée ne contient aucun collaborateur.")
            
            typer.echo(f"[ID] : {user.id} -- [Identité] : {user.identity} -- [Email] : {user.email} -- [Departement] : {user.department.name}")
            
    typer.echo("Action restricted.")


@app.command()
def show_all_clients():
    queryset = Client.select()
    
    for client in queryset:
        if queryset.len() == 0:
            typer.echo("La base de donnée ne contient aucun client.")
        
        typer.echo(f"[ID] : {client.id} -- [Identité] : {client.identity} -- [Email] : {client.email} -- [Téléphone] : {client.phone} -- [Entreprise] : {client.company.name} -- [Date de création] : {client.creation_date} -- [Dernier contact] : {client.last_update} -- Commercial associé : {client.collaborator.identity}")


@app.command()
def show_all_contracts():
    queryset = Contract.select()
    
    for contract in queryset:
        if queryset.len() == 0:
            typer.echo("La base de donnée ne contient aucun contrat.")
        
        typer.echo(f"[ID] : {contract.id} -- [Client] : {contract.client.identity} -- [Commercial associé] : {contract.collaborator.identity} -- [Montant total] : {contract.total_sum} -- [Montant restant dû] : {contract.amount_due} -- [Date de création] : {contract.creation_date} -- [Contrat signé ?] : {contract.signed}")


@app.command()
def show_all_events():
    queryset = Event.select()
    
    for event in queryset:
        if queryset.len() == 0:
            typer.echo("La base de donnée ne contient aucun évènement.")
        
        typer.echo(f"[ID] : {event.id} -- [ID Contrat] : {event.contract.id} -- [Client] : {event.contract.client.identity} -- [Date de début] : {event.start_date} -- [Date de fin] : {event.end_date} -- [Localisation] : {event.location} -- [Nombre de participants] : {event.attendees} --  [Notes] : {event.notes} -- [Assistant en charge] : {event.collaborator.identity}")


@app.command()
def create_collaborator(identity: str, email: str, password: str, department: int):
    if collaborator.department == 1:
        Collaborator.create(identity=identity, email=email, password=password, department=department)
        typer.echo(f"Collaborator {identity} created successfully.")

    typer.echo("Action restricted.")


if __name__ == "__main__":
    app()