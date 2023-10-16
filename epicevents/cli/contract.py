import typer
from epicevents.data_access_layer.contract import Contract
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