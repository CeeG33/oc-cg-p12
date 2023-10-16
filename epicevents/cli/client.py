import os, typer
from dotenv import load_dotenv
from epicevents.data_access_layer.client import Client
from .collaborator import _verify_token


app = typer.Typer()


@app.command()
def list():
    token_check = _verify_token()
    if token_check:
        queryset = Client.select()
    
        for client in queryset:
            if len(Client) == 0:
                typer.echo("La base de donnée ne contient aucun client.")
            
            else:
                typer.echo(f"[ID] : {client.id} -- [Prénom] : {client.first_name} -- [Nom] : {client.name} -- [Email] : {client.email} -- [Téléphone] : {client.phone} -- [Entreprise] : {client.company.name} -- [Date de création] : {client.creation_date} -- [Dernier contact] : {client.last_update} -- Commercial associé : {client.collaborator.first_name} {client.collaborator.name}")
    
    else:    
        typer.echo("Veuillez vous authentifier et réessayer.")