import typer
from epicevents.data_access_layer.event import Event
from .collaborator import _verify_token


app = typer.Typer()


@app.command()
def show_all_events():
    if _verify_token():
        queryset = Event.select()
        
        for event in queryset:
            if queryset.len() == 0:
                typer.echo("La base de donnée ne contient aucun évènement.")
            
            typer.echo(f"[ID] : {event.id} -- [ID Contrat] : {event.contract.id} -- [Client] : {event.contract.client.identity} -- [Date de début] : {event.start_date} -- [Date de fin] : {event.end_date} -- [Localisation] : {event.location} -- [Nombre de participants] : {event.attendees} --  [Notes] : {event.notes} -- [Assistant en charge] : {event.collaborator.identity}")
    
    typer.echo("Veuillez vous authentifier.")