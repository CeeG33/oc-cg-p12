import typer
from peewee import DoesNotExist
from typing_extensions import Annotated, Optional
from epicevents.data_access_layer.event import Event
from epicevents.data_access_layer.collaborator import Collaborator
from epicevents.data_access_layer.contract import Contract
from epicevents.cli import collaborator as clicollaborator
from epicevents.cli.collaborator import (
    MANAGEMENT_DEPARTMENT_ID,
    SALES_DEPARTMENT_ID,
    SUPPORT_DEPARTMENT_ID,
)
from .collaborator import _verify_token


app = typer.Typer()


@app.command()
def list():
    """Lists all events."""
    token_check = clicollaborator._verify_token()
    if token_check:
        queryset = Event.select()

        for event in queryset:
            if len(Event) == 0:
                print("La base de donnée ne contient aucun évènement.")
                raise typer.Exit()

            else:
                print(
                    f"[ID] : {event.id} -- [ID Contrat] : {event.contract.id} -- [Client] : {event.contract.client.first_name} {event.contract.client.name} -- [Date de début] : {event.start_date} -- [Date de fin] : {event.end_date} -- [Localisation] : {event.location} -- [Nombre de participants] : {event.attendees} --  [Notes] : {event.notes} -- [Assistant en charge] : {event.support.first_name} {event.support.name}"
                )

    else:
        print("Veuillez vous authentifier et réessayer.")
        raise typer.Exit()


@app.command()
def filter(s: Annotated[bool, typer.Option("-s", help="Filtre les évènements qui n'ont pas de support affecté")] = False):
    """Filters the events depending on the option selected."""
    token_check = clicollaborator._verify_token()
    if token_check:
        collaborator_department = token_check[1]["department_id"]
        collaborator_id = token_check[1]["collaborator_id"]

        if int(collaborator_department) in [
            MANAGEMENT_DEPARTMENT_ID,
            SUPPORT_DEPARTMENT_ID,
        ]:
            if s:
                if int(collaborator_department) == MANAGEMENT_DEPARTMENT_ID:
                    queryset = Event.select().where(Event.support == None)

                    for event in queryset:
                        print(
                            f"[ID] : {event.id} -- [ID Contrat] : {event.contract.id} -- [Client] : {event.contract.client.first_name} {event.contract.client.name} -- [Date de début] : {event.start_date} -- [Date de fin] : {event.end_date} -- [Localisation] : {event.location} -- [Nombre de participants] : {event.attendees} --  [Notes] : {event.notes} -- [Assistant en charge] : À définir"
                        )

                elif int(collaborator_department) == SUPPORT_DEPARTMENT_ID:
                    support = Collaborator.get(Collaborator.id == collaborator_id)
                    queryset = Event.select().where(Event.support == support)

                    for event in queryset:
                        print(
                            f"[ID] : {event.id} -- [ID Contrat] : {event.contract.id} -- [Client] : {event.contract.client.first_name} {event.contract.client.name} -- [Date de début] : {event.start_date} -- [Date de fin] : {event.end_date} -- [Localisation] : {event.location} -- [Nombre de participants] : {event.attendees} --  [Notes] : {event.notes} -- [Assistant en charge] : {event.support.first_name} {event.support.name}"
                        )

            elif not s:
                print("Vous n'avez pas sélectionné de filtre à appliquer.")
                raise typer.Exit()

        else:
            print("Action restreinte.")
            raise typer.Exit()

    else:
        print("Veuillez vous authentifier et réessayer.")
        raise typer.Exit()


@app.command()
def update(
    event_id: Annotated[int, typer.Argument(help="N° de l'évènement à modifier - Exemple : 1")],
    new_value: Annotated[str, typer.Argument(help="Nouvelle valeur à appliquer - La valeur doit être compatible avec le champ modifié !")],
    contract: Annotated[bool, typer.Option("-c", help="Modifier le numéro du contrat - Exemple : 1")] = False,
    start_date: Annotated[bool, typer.Option("-d", help="Modifier la date de début - Exemple : 2023-12-24")] = False,
    end_date: Annotated[bool, typer.Option("-ed", help="Modifier la date de fin - Exemple : 2023-12-24")] = False,
    location: Annotated[bool, typer.Option("-l", help="Modifier la localisation - Exemple : 42, rue du Vieux Pont - 92000 NANTERRE")] = False,
    attendees: Annotated[bool, typer.Option("-a", help="Modifier le nombre de participants - Exemple : 4")] = False,
    notes: Annotated[bool, typer.Option("-n", help="Modifier les notes - Exemple : Prévoir des bouteilles d'eau")] = False,
    support: Annotated[bool, typer.Option("-s", help="Modifier le numéro du support associé - Exemple : 1")] = False,
):
    """Updates a given event."""
    token_check = clicollaborator._verify_token()
    if token_check:
        collaborator_department = token_check[1]["department_id"]
        collaborator_id = token_check[1]["collaborator_id"]
        try:
            event = Event.get(Event.id == event_id)

        except DoesNotExist:
            print(f"Aucun évènement trouvé avec l'ID n°{event_id}.")
            raise typer.Exit()

        if (int(collaborator_department) == MANAGEMENT_DEPARTMENT_ID) or (
            int(collaborator_department) == SUPPORT_DEPARTMENT_ID
            and int(collaborator_id) == event.support.id
        ):
            if contract:
                contract_check = Contract.get_or_none(Contract.id == new_value)

                if contract_check:
                    event.contract = new_value
                    event.save()
                    print(
                        f"Le champ 'Contrat' de l'évènement n°{event_id} a été mis à jour avec succès."
                    )

                else:
                    print("Veuillez entrer un numéro de contrat valide.")
                    raise typer.Exit(code=1)

            elif support:
                support_check = Collaborator.get_or_none(Collaborator.id == new_value)

                if (
                    support_check
                    and support_check.department.id == SUPPORT_DEPARTMENT_ID
                ):
                    event.support = new_value
                    event.save()
                    print(
                        f"Le champ 'Assistant en charge' de l'évènement n°{event_id} a été mis à jour avec succès."
                    )

                else:
                    print(
                        "Veuillez entrer un numéro de collaborateur valide et faisant partie du département Support."
                    )
                    raise typer.Exit(code=1)

            elif start_date:
                event.start_date = new_value
                event.save()
                print(
                    f"Le champ 'Date de début' de l'évènement n°{event_id} a été mis à jour avec succès."
                )
                print("Veuillez également penser à modifier la date de fin.")

            elif end_date:
                event.end_date = new_value
                event.save()
                print(
                    f"Le champ 'Date de fin' de l'évènement n°{event_id} a été mis à jour avec succès."
                )
                print("Avez-vous également pensé à modifier la date de début ?")

            elif location:
                event.location = new_value
                event.save()
                print(
                    f"Le champ 'Localisation' de l'évènement n°{event_id} a été mis à jour avec succès."
                )

            elif attendees:
                event.attendees = new_value
                event.save()
                print(
                    f"Le champ 'Nombre de participants' de l'évènement n°{event_id} a été mis à jour avec succès."
                )

            elif notes:
                event.notes = new_value
                event.save()
                print(
                    f"Le champ 'Notes' de l'évènement n°{event_id} a été mis à jour avec succès."
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
def create(
    contract: Annotated[int, typer.Option(prompt="N° du contrat", help="Numéro du contrat associé - Exemple : 1")],
    start_date: Annotated[str, typer.Option(prompt="Date de début", help="Date de début - Exemple : 2023-12-24")],
    end_date: Annotated[str, typer.Option(prompt="Date de fin", help="Date de fin - Exemple : 2023-12-24")],
    location: Annotated[str, typer.Option(prompt="Localisation", help="Localisation - Exemple : 42, rue du Vieux Pont - 92000 NANTERRE")],
    attendees: Annotated[int, typer.Option(prompt="Nombre de participants", help="Nombre de participants - Exemple : 4")],
    notes: Annotated[str, typer.Option(help="Notes - Exemple : Prévoir des bouteilles d'eau")] = "",
    support: Annotated[int, typer.Option(help="Numéro du support associé - Exemple : 2")] = None,
):
    """Creates a new event."""
    token_check = clicollaborator._verify_token()
    if token_check:
        collaborator_department = token_check[1]["department_id"]
        collaborator_id = token_check[1]["collaborator_id"]

        if int(collaborator_department) == SALES_DEPARTMENT_ID:
            target_contract = Contract.get_or_none(Contract.id == contract)

            if target_contract:
                if target_contract.client.collaborator.id != collaborator_id:
                    print(
                        "Vous ne pouvez pas créer d'évènement pour un client qui ne vous est pas affecté."
                    )
                    raise typer.Exit()

                if target_contract.signed == False:
                    print(
                        "Vous ne pouvez pas créer d'évènement pour un contrat qui n'est pas signé."
                    )
                    raise typer.Exit()
                
            else:
                print("Veuillez entrer un numéro de contrat valide.")
                raise typer.Exit()
            
            if support is not None:
                support_check = Collaborator.get_or_none(Collaborator.id == support)
                
                if not support_check:
                    print("Veuillez entrer un numéro de support valide.")
                    raise typer.Exit()

            Event.create(
                contract=target_contract.id,
                start_date=start_date,
                end_date=end_date,
                location=location,
                attendees=attendees,
                notes=notes,
                support=support,
            )
            print("L'évènement a été créé avec succès.")

        else:
            print("Action restreinte.")
            raise typer.Exit()

    else:
        print("Veuillez vous authentifier et réessayer.")
        raise typer.Exit()


if __name__ == "__main__":
    app()
