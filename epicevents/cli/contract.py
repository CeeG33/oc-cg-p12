import typer
from epicevents.data_access_layer.contract import Contract
from epicevents.cli.collaborator import MANAGEMENT_DEPARTMENT_ID, SALES_DEPARTMENT_ID, SUPPORT_DEPARTMENT_ID
from .collaborator import _verify_token


app = typer.Typer()


@app.command()
def list():
    token_check = _verify_token()
    if token_check:
        
        queryset = Contract.select()
        
        for contract in queryset:
            if len(Contract) == 0:
                typer.echo("La base de donnée ne contient aucun contrat.")
            
            else:
                typer.echo(f"[ID] : {contract.id} -- [Client] : {contract.client.first_name} {contract.client.name} -- [Commercial associé] : {contract.collaborator.first_name} {contract.collaborator.name} -- [Montant total] : {contract.total_sum} -- [Montant restant dû] : {contract.amount_due} -- [Date de création] : {contract.creation_date} -- [Contrat signé ?] : {contract.signed}")
    
    else:
        typer.echo("Veuillez vous authentifier et réessayer.")

## CONTINUER ICI
@app.command()
def create(first_name: str, name: str, email: str, password: str, department: int):
    token_check = _verify_token()
    if token_check:
        collaborator_department = token_check[1]["department_id"]
        
        if int(collaborator_department) == MANAGEMENT_DEPARTMENT_ID:
            Contract.create(first_name=first_name, name=name, email=email, password=password, department=department) # A ADAPTER POUR CONTRAT
            typer.echo(f"Le contrat a été créé avec succès.")
        
        else:
            typer.echo("Action restreinte.")
        
    else:
        typer.echo("Veuillez vous authentifier et réessayer.")


## CONTINUER ICI
@app.command()
def update(contract_id: int):
    token_check = _verify_token()
    if token_check:
        collaborator_department = token_check[1]["department_id"]
        
        if int(collaborator_department) == MANAGEMENT_DEPARTMENT_ID:
            ## Ecrire la commande qui MAJ le contrat
            typer.echo(f"Le contrat a été mis à jour avec succès.")
        
        else:
            typer.echo("Action restreinte.")
        
    else:
        typer.echo("Veuillez vous authentifier et réessayer.")