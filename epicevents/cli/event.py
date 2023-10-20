import typer
from peewee import DoesNotExist
from typing_extensions import Annotated, Optional
from epicevents.data_access_layer.event import Event
from epicevents.data_access_layer.collaborator import Collaborator
from epicevents.cli import collaborator as clicollaborator
from epicevents.cli.collaborator import MANAGEMENT_DEPARTMENT_ID, SALES_DEPARTMENT_ID, SUPPORT_DEPARTMENT_ID
from .collaborator import _verify_token


app = typer.Typer()


@app.command()
def list():
    token_check = clicollaborator._verify_token()
    if token_check:
        
        queryset = Event.select()
        
        for event in queryset:
            if len(Event) == 0:
                typer.echo("La base de donnée ne contient aucun évènement.")
            
            else:
                typer.echo(f"[ID] : {event.id} -- [ID Contrat] : {event.contract.id} -- [Client] : {event.contract.client.first_name} {event.contract.client.name} -- [Date de début] : {event.start_date} -- [Date de fin] : {event.end_date} -- [Localisation] : {event.location} -- [Nombre de participants] : {event.attendees} --  [Notes] : {event.notes} -- [Assistant en charge] : {event.support.first_name} {event.support.name}")
    
    else:
        typer.echo("Veuillez vous authentifier.")


@app.command()
def filter(s: Annotated[bool, typer.Option()] = False):
    token_check = clicollaborator._verify_token()
    if token_check:
        collaborator_department = token_check[1]["department_id"]
        collaborator_id = token_check[1]["collaborator_id"]
        
        if (int(collaborator_department) in [MANAGEMENT_DEPARTMENT_ID, SUPPORT_DEPARTMENT_ID]):
            if s:
                if (int(collaborator_department) == MANAGEMENT_DEPARTMENT_ID):
                    queryset = Event.select().where(Event.support == None)
                    
                    for event in queryset:
                        print(f"[ID] : {event.id} -- [ID Contrat] : {event.contract.id} -- [Client] : {event.contract.client.first_name} {event.contract.client.name} -- [Date de début] : {event.start_date} -- [Date de fin] : {event.end_date} -- [Localisation] : {event.location} -- [Nombre de participants] : {event.attendees} --  [Notes] : {event.notes} -- [Assistant en charge] : À définir")
                
                elif (int(collaborator_department) == SUPPORT_DEPARTMENT_ID):
                    support = Collaborator.get(Collaborator.id == collaborator_id)
                    queryset = Event.select().where(Event.support == support)
                    
                    for event in queryset:
                        print(f"[ID] : {event.id} -- [ID Contrat] : {event.contract.id} -- [Client] : {event.contract.client.first_name} {event.contract.client.name} -- [Date de début] : {event.start_date} -- [Date de fin] : {event.end_date} -- [Localisation] : {event.location} -- [Nombre de participants] : {event.attendees} --  [Notes] : {event.notes} -- [Assistant en charge] : {event.support.first_name} {event.support.name}")
            
            elif not s:
                print("Vous n'avez pas sélectionné de filtre à appliquer.")
                raise typer.Exit()
            
        else:
            print("Action restreinte.")
            raise typer.Exit()
            
    else:
        print("Veuillez vous authentifier et réessayer.")
        raise typer.Exit()


if __name__ == "__main__":
    app()