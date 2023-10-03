import typer
from epicevents.data_access_layer.client import Client
from .collaborator import _verify_token


app = typer.Typer()


@app.command()
def show_all_clients():
    if _verify_token():
        queryset = Client.select()
    
        for client in queryset:
            if queryset.len() == 0:
                typer.echo("La base de donnée ne contient aucun client.")
            
            typer.echo(f"[ID] : {client.id} -- [Identité] : {client.identity} -- [Email] : {client.email} -- [Téléphone] : {client.phone} -- [Entreprise] : {client.company.name} -- [Date de création] : {client.creation_date} -- [Dernier contact] : {client.last_update} -- Commercial associé : {client.collaborator.identity}")
        
    typer.echo("Veuillez vous authentifier.")