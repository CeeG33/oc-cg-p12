import os, typer
from peewee import DoesNotExist
from datetime import datetime
from typing_extensions import Annotated
from dotenv import load_dotenv
from epicevents.data_access_layer.client import Client
from epicevents.data_access_layer.company import Company
from epicevents.cli import collaborator as clicollaborator
from epicevents.cli.collaborator import MANAGEMENT_DEPARTMENT_ID, SALES_DEPARTMENT_ID, SUPPORT_DEPARTMENT_ID
from .collaborator import _verify_token


app = typer.Typer()


@app.command()
def list():
    token_check = clicollaborator._verify_token()
    if token_check:
        queryset = Client.select()
    
        for client in queryset:
            if len(Client) == 0:
                print("La base de donnée ne contient aucun client.")
                raise typer.Exit
            
            else:
                print(f"[ID] : {client.id} -- [Prénom] : {client.first_name} -- [Nom] : {client.name} -- [Email] : {client.email} -- [Téléphone] : {client.phone} -- [Entreprise] : {client.company.name} -- [Date de création] : {client.creation_date} -- [Dernier contact] : {client.last_update} -- Commercial associé : {client.collaborator.first_name} {client.collaborator.name}")
                raise typer.Exit
    
    else:    
        print("Veuillez vous authentifier et réessayer.")
        raise typer.Exit


@app.command()
def create(first_name: Annotated[str, typer.Argument()],
           name: Annotated[str, typer.Argument()],
           email: Annotated[str, typer.Argument()],
           phone: Annotated[str, typer.Argument()],
           company: Annotated[int, typer.Argument()],
           collaborator: Annotated[int, typer.Argument()] = 0,
           creation_date: Annotated[str, typer.Argument()] = datetime.now().date(),
           last_update: Annotated[int, typer.Argument()] = datetime.now().date()
        ):
    token_check = clicollaborator._verify_token()
    if token_check:
        collaborator_department = token_check[1]["department_id"]
        collaborator_id = token_check[1]["collaborator_id"]
        
        if int(collaborator_department) == SALES_DEPARTMENT_ID:
            company_check = Company.get_or_none(Company.id == company)
                
            if company_check is None:
                print(f"Aucune entreprise trouvée avec l'ID n°{company}.")
                raise typer.Exit()
            
            Client.create(first_name=first_name, name=name, email=email, phone=phone, company=company_check.id, collaborator=collaborator_id, creation_date=creation_date, last_update=last_update)
            print("Le client a été créé avec succès.")
        
        else:
            print("Action restreinte.")
            raise typer.Exit()
        
    else:
        print("Veuillez vous authentifier et réessayer.")
        raise typer.Exit()
    
@app.command()
def update(client_id: Annotated[int, typer.Argument()],
           new_value: Annotated[str, typer.Argument()], 
           first_name: Annotated[bool, typer.Option()] = False,
           name: Annotated[bool, typer.Option()] = False,
           email: Annotated[bool, typer.Option()] = False,
           phone: Annotated[bool, typer.Option()] = False,
           company: Annotated[bool, typer.Option()] = False,
           creation_date: Annotated[bool, typer.Option()] = False,
           last_update: Annotated[bool, typer.Option()] = False
        ):
    token_check = clicollaborator._verify_token()
    if token_check:
        collaborator_department = token_check[1]["department_id"]
        collaborator_id = token_check[1]["collaborator_id"]
        try:
            client = Client.get(Client.id == client_id)
                
        except DoesNotExist:
            print(f"Aucun évènement trouvé avec l'ID n°{client_id}.")
            raise typer.Exit()
                
        if (int(collaborator_department) == SALES_DEPARTMENT_ID and int(collaborator_id) == client.collaborator.id):

            if company:
                company_check = Company.get_or_none(Company.id == new_value)
                
                if company_check:
                    client.company = new_value
                    client.save()
                    print(f"Le champ 'Entreprise' du client n°{client_id} a été mis à jour avec succès.")
                
                else:
                    print("Veuillez entrer un numéro d'entreprise valide.")
                    raise typer.Exit(code=1)
                
            elif first_name:
                client.first_name = new_value
                client.save()
                print(f"Le champ 'Prénom' du client n°{client_id} a été mis à jour avec succès.")
                
            elif name:
                client.name = new_value
                client.save()
                print(f"Le champ 'Nom' du client n°{client_id} a été mis à jour avec succès.")
                
            elif email:
                client.email = new_value
                client.save()
                print(f"Le champ 'Email' du client n°{client_id} a été mis à jour avec succès.")
                
            elif phone:
                client.phone = new_value
                client.save()
                print(f"Le champ 'Téléphone' du client n°{client_id} a été mis à jour avec succès.")
                
            elif creation_date:
                client.creation_date = new_value
                client.save()
                print(f"Le champ 'Date de création' du client n°{client_id} a été mis à jour avec succès.")
            
            elif last_update:
                client.last_update = new_value
                client.save()
                print(f"Le champ 'Dernier contact' du client n°{client_id} a été mis à jour avec succès.")
                
            else:
                print("Vous n'avez pas sélectionné d'attribut à modifier.")
                raise typer.Exit()
            
        else:
            print("Action restreinte.")
            raise typer.Exit()
        
    else:
        print("Veuillez vous authentifier et réessayer.")
        raise typer.Exit()