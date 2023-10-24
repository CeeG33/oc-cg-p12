import typer
from typing_extensions import Annotated
from peewee import DoesNotExist
from datetime import datetime
from epicevents.sentry import sentry_sdk
from epicevents.data_access_layer.contract import Contract
from epicevents.data_access_layer.client import Client
from epicevents.data_access_layer.collaborator import Collaborator
from epicevents.cli import collaborator as clicollaborator
from epicevents.cli.collaborator import (
    MANAGEMENT_DEPARTMENT_ID,
    SALES_DEPARTMENT_ID,
    SUPPORT_DEPARTMENT_ID,
    _verify_token,
)


app = typer.Typer()


@app.command()
def list():
    """Lists all contracts."""
    token_check = clicollaborator._verify_token()
    if token_check:
        queryset = Contract.select()

        for contract in queryset:
            if len(Contract) == 0:
                print("La base de donnée ne contient aucun contrat.")

            else:
                print(
                    f"[ID] : {contract.id} -- [Client] : {contract.client.first_name} {contract.client.name} -- [Commercial associé] : {contract.collaborator.first_name} {contract.collaborator.name} -- [Montant total] : {contract.total_sum} -- [Montant restant dû] : {contract.amount_due} -- [Date de création] : {contract.creation_date} -- [Contrat signé ?] : {contract.signed}"
                )

    else:
        print("Veuillez vous authentifier et réessayer.")
        raise typer.Exit()


@app.command()
def create(
    client: Annotated[int, typer.Option(prompt="N° du client", help="Numéro du client - Exemple : 2")],
    collaborator: Annotated[int, typer.Option(prompt="N° du commercial", help="Numéro du commercial en charge - Exemple : 2")],
    total_sum: Annotated[float, typer.Option(prompt="Montant total", help="Montant total - Exemple : 1000")],
    amount_due: Annotated[float, typer.Option(prompt="Montant restant dû", help="Montant restant dû - Exemple : 1000")] = None,
    creation_date: Annotated[str, typer.Option(help="Date de création - Exemple : 2023-12-24")] = datetime.now().date(),
    signed: Annotated[bool, typer.Option(help="Statut de la signature - Rappel : True pour Signé / False pour Non signé")] = False,
):
    """Creates a new contract."""
    token_check = clicollaborator._verify_token()
    if token_check:
        collaborator_department = token_check[1]["department_id"]

        if int(collaborator_department) == MANAGEMENT_DEPARTMENT_ID:
            client_check = Client.get_or_none(Client.id == client)
            collaborator_check = Collaborator.get_or_none(Collaborator.id == collaborator)

            if client_check is None:
                print(f"Aucun client trouvé avec l'ID n°{client}.")
                raise typer.Exit()
            
            if collaborator_check is None:
                print(f"Aucun commercial trouvé avec l'ID n°{collaborator}.")
                raise typer.Exit()
            
            Contract.create(
                client=client,
                collaborator=collaborator,
                total_sum=total_sum,
                amount_due=amount_due,
                creation_date=creation_date,
                signed=signed,
            )
            print("Le contrat a été créé avec succès.")

        else:
            print("Action restreinte.")
            raise typer.Exit()

    else:
        print("Veuillez vous authentifier et réessayer.")
        raise typer.Exit()


@app.command()
def update(
    contract_id: Annotated[int, typer.Argument(help="N° du contrat à modifier - Exemple : 1")],
    new_value: Annotated[str, typer.Argument(help="Nouvelle valeur à appliquer - La valeur doit être compatible avec le champ modifié !")],
    client: Annotated[bool, typer.Option("-c", help="Modifier le numéro du client - Exemple : 1")] = False,
    collaborator: Annotated[bool, typer.Option("-col", help="Modifier le numéro du commercial rattaché - Exemple : 1")] = False,
    total_sum: Annotated[bool, typer.Option("-s", help="Modifier le montant total - Exemple : 1000")] = False,
    amount_due: Annotated[bool, typer.Option("-sd", help="Modifier le montant restant dû - Exemple : 1000")] = False,
    creation_date: Annotated[bool, typer.Option("-d", help="Modifier la date de création - Exemple : 2023-12-24")] = False,
    signed: Annotated[bool, typer.Option("-e", help="Modifier le statut de la signature - Rappel : True pour Signé / False pour Non signé")] = False,
):
    """Updates a given contract."""
    token_check = clicollaborator._verify_token()
    if token_check:
        collaborator_department = token_check[1]["department_id"]
        collaborator_id = token_check[1]["collaborator_id"]
        try:
            contract = Contract.get(Contract.id == contract_id)

        except DoesNotExist:
            print(f"Aucun contrat trouvé avec l'ID n°{contract_id}.")
            raise typer.Exit()

        if (int(collaborator_department) == MANAGEMENT_DEPARTMENT_ID) or (
            int(collaborator_department) == SALES_DEPARTMENT_ID
            and int(collaborator_id) == contract.client.collaborator.id
        ):
            if client:
                client_check = Client.get_or_none(Client.id == new_value)

                if client_check:
                    contract.client = new_value
                    contract.save()
                    print(
                        f"Le champ 'Client' du contrat n°{contract_id} a été mis à jour avec succès."
                    )

                else:
                    print("Veuillez entrer un numéro de client valide.")
                    raise typer.Exit(code=1)

            elif collaborator:
                collaborator_check = Collaborator.get_or_none(
                    Collaborator.id == new_value
                )

                if collaborator_check:
                    contract.collaborator = new_value
                    contract.save()
                    print(
                        f"Le champ 'Collaborateur' du contrat n°{contract_id} a été mis à jour avec succès."
                    )

                else:
                    print("Veuillez entrer un numéro de collaborateur valide.")
                    raise typer.Exit(code=1)

            elif total_sum:
                contract.total_sum = new_value
                contract.save()
                print(
                    f"Le champ 'Montant total' du contrat n°{contract_id} a été mis à jour avec succès."
                )

            elif amount_due:
                contract.amount_due = new_value
                contract.save()
                print(
                    f"Le champ 'Montant dû' du contrat n°{contract_id} a été mis à jour avec succès."
                )

            elif creation_date:
                contract.creation_date = new_value
                contract.save()
                print(
                    f"Le champ 'Date de création' du contrat n°{contract_id} a été mis à jour avec succès."
                )

            elif signed:
                contract.signed = new_value
                contract.save()
                print(
                    f"Le champ 'Signé' du contrat n°{contract_id} a été mis à jour avec succès."
                )
                sentry_sdk.capture_message(
                    f"[SIGNATURE CONTRAT N°{contract_id} PAR COLLABORATEUR N°{collaborator_id}] >> Date : {datetime.now()}"
                )

            else:
                print("Vous n'avez pas sélectionné d'attribut à modifier.")
                raise typer.Exit()

        else:
            print("Action restreinte.")
            raise typer.Exit()

    else:
        print("Veuillez vous authentifier et réessayer.")
        raise typer.Exit()


@app.command()
def filter(
    ns: Annotated[bool, typer.Option("-ns", help="Filtre les contrats non signés")] = False,
    u: Annotated[bool, typer.Option("-u", help="Filtre les contrats non payés en totalité")] = False,
):
    """Filters the contracts depending on the option selected."""
    token_check = clicollaborator._verify_token()
    if token_check:
        collaborator_department = token_check[1]["department_id"]

        if int(collaborator_department) == SALES_DEPARTMENT_ID:
            if ns:
                queryset = Contract.select().where(Contract.signed == False)

                for contract in queryset:
                    print(
                        f"[ID] : {contract.id} -- [Client] : {contract.client.first_name} {contract.client.name} -- [Commercial associé] : {contract.collaborator.first_name} {contract.collaborator.name} -- [Montant total] : {contract.total_sum} -- [Montant restant dû] : {contract.amount_due} -- [Date de création] : {contract.creation_date} -- [Contrat signé ?] : {contract.signed}"
                    )

            if u:
                queryset = Contract.select().where(
                    (Contract.amount_due > 0) | (Contract.amount_due == None)
                )

                for contract in queryset:
                    print(
                        f"[ID] : {contract.id} -- [Client] : {contract.client.first_name} {contract.client.name} -- [Commercial associé] : {contract.collaborator.first_name} {contract.collaborator.name} -- [Montant total] : {contract.total_sum} -- [Montant restant dû] : {contract.amount_due} -- [Date de création] : {contract.creation_date} -- [Contrat signé ?] : {contract.signed}"
                    )

            elif not (ns or u):
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
