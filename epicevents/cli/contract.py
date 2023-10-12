import typer
from epicevents.data_access_layer.contract import Contract
from .collaborator import _verify_token


app = typer.Typer()


@app.command()
def list():
    if _verify_token():
        
        queryset = Contract.select()
        
        for contract in queryset:
            if queryset.len() == 0:
                typer.echo("La base de donnée ne contient aucun contrat.")
            
            typer.echo(f"[ID] : {contract.id} -- [Client] : {contract.client.identity} -- [Commercial associé] : {contract.collaborator.identity} -- [Montant total] : {contract.total_sum} -- [Montant restant dû] : {contract.amount_due} -- [Date de création] : {contract.creation_date} -- [Contrat signé ?] : {contract.signed}")
    
    typer.echo("Veuillez vous authentifier.")