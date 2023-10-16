import typer
from epicevents.data_access_layer.event import Event
from .collaborator import _verify_token


app = typer.Typer()


@app.command()
def list():
    token_check = _verify_token()
    if token_check:
        
        queryset = Event.select()
        
        for event in queryset:
            if len(Event) == 0:
                typer.echo("La base de donnée ne contient aucun évènement.")
            
            else:
                typer.echo(f"[ID] : {event.id} -- [ID Contrat] : {event.contract.id} -- [Client] : {event.contract.client.first_name} {event.contract.client.name} -- [Date de début] : {event.start_date} -- [Date de fin] : {event.end_date} -- [Localisation] : {event.location} -- [Nombre de participants] : {event.attendees} --  [Notes] : {event.notes} -- [Assistant en charge] : {event.support.first_name} {event.support.name}")
    
    else:
        typer.echo("Veuillez vous authentifier.")