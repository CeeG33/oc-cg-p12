import os, typer
from rich import print
from rich.console import Console
from rich.table import Table
from peewee import DoesNotExist
from datetime import datetime
from typing_extensions import Annotated
from dotenv import load_dotenv
from epicevents.data_access_layer.client import Client
from epicevents.data_access_layer.company import Company
from epicevents.cli import collaborator as clicollaborator
from epicevents.cli.collaborator import (
    MANAGEMENT_DEPARTMENT_ID,
    SALES_DEPARTMENT_ID,
    SUPPORT_DEPARTMENT_ID,
)
from .collaborator import _verify_token


app = typer.Typer()


def _create_clients_table():
    table = Table(title="Tableau des clients")
    table.add_column("[ID]", justify="center", no_wrap=True, style="cyan")
    table.add_column("[Prénom]", justify="center", no_wrap=True, style="orange_red1")
    table.add_column("[Nom]", justify="center", no_wrap=True, style="orange_red1")
    table.add_column("[Email]", justify="center", no_wrap=True, style="yellow")
    table.add_column("[Téléphone]", justify="center", no_wrap=True, style="yellow")
    table.add_column("[Entreprise]", justify="center", no_wrap=True, style="plum4")
    table.add_column(
        "[Date de création]", justify="center", no_wrap=True, style="purple4"
    )
    table.add_column(
        "[Dernier contact]", justify="center", no_wrap=True, style="purple4"
    )
    table.add_column(
        "[Commercial associé]", justify="center", no_wrap=True, style="blue"
    )

    return table


def _add_rows_in_clients_table(client, table):
    table.add_row(
        f"{client.id}",
        f"{client.first_name}",
        f"{client.name}",
        f"{client.email}",
        f"{client.phone}",
        f"{client.company.name}",
        f"{client.creation_date} ",
        f"{client.last_update}",
        f"{client.collaborator.first_name} {client.collaborator.name}",
    )


def _print_table(queryset):
    table = _create_clients_table()

    for client in queryset:
        _add_rows_in_clients_table(client, table)

    console = Console()
    console.print(table)


@app.command()
def list():
    """Lists all clients."""
    token_check = clicollaborator._verify_token()
    if token_check:
        queryset = Client.select()

        if len(queryset) == 0:
            print("La base de donnée ne contient aucun client.")
            raise typer.Exit()

        _print_table(queryset)

    else:
        print("Veuillez vous authentifier et réessayer.")
        raise typer.Exit()


@app.command()
def create(
    first_name: Annotated[
        str, typer.Option(prompt="Prénom", help="Prénom du client - Exemple : Alain")
    ],
    name: Annotated[
        str, typer.Option(prompt="Nom", help="Nom du client - Exemple : Terieur")
    ],
    email: Annotated[
        str,
        typer.Option(
            prompt="Email",
            help="Adresse mail du client - Exemple : alain.terieur@mail.com",
        ),
    ],
    phone: Annotated[
        str,
        typer.Option(
            prompt="Téléphone",
            help="Numéro de téléphone du client - Exemple : 0654987845",
        ),
    ],
    company: Annotated[
        int,
        typer.Option(
            prompt="N° d'entreprise", help="Numéro d'entreprise du client - Exemple : 2"
        ),
    ],
    creation_date: Annotated[
        str, typer.Option(help="Date de création - Exemple : 2023-12-24")
    ] = datetime.now().date(),
    last_update: Annotated[
        str, typer.Option(help="Dernier contact - Exemple : 2023-12-24")
    ] = datetime.now().date(),
    collaborator: Annotated[
        int, typer.Option(help="Numéro du commercial en charge - Exemple : 1")
    ] = 0,
):
    """Creates a new client."""
    token_check = clicollaborator._verify_token()
    if token_check:
        collaborator_department = token_check[1]["department_id"]
        collaborator_id = token_check[1]["collaborator_id"]

        if int(collaborator_department) == SALES_DEPARTMENT_ID:
            company_check = Company.get_or_none(Company.id == company)

            if company_check is None:
                print(f"Aucune entreprise trouvée avec l'ID n°{company}.")
                raise typer.Exit()

            Client.create(
                first_name=first_name,
                name=name,
                email=email,
                phone=phone,
                company=company_check.id,
                collaborator=collaborator_id,
                creation_date=creation_date,
                last_update=last_update,
            )
            print("Le client a été créé avec succès.")

        else:
            print("Action restreinte.")
            raise typer.Exit()

    else:
        print("Veuillez vous authentifier et réessayer.")
        raise typer.Exit()


@app.command()
def update(
    client_id: Annotated[
        int, typer.Argument(help="N° du client à modifier - Exemple : 1")
    ],
    new_value: Annotated[
        str,
        typer.Argument(
            help="Nouvelle valeur à appliquer - La valeur doit être compatible avec le champ modifié !"
        ),
    ],
    first_name: Annotated[
        bool, typer.Option("-fn", help="Modifier le prénom - Exemple : Alain")
    ] = False,
    name: Annotated[
        bool, typer.Option("-n", help="Modifier le nom - Exemple : Terieur")
    ] = False,
    email: Annotated[
        bool,
        typer.Option("-e", help="Modifier l'email - Exemple : alain.terieur@mail.com"),
    ] = False,
    phone: Annotated[
        bool,
        typer.Option(
            "-p", help="Modifier le numéro de téléphone - Exemple : 0654987845"
        ),
    ] = False,
    company: Annotated[
        bool, typer.Option("-c", help="Modifier le numéro d'entreprise - Exemple : 1")
    ] = False,
    creation_date: Annotated[
        bool,
        typer.Option("-d", help="Modifier la date de création - Exemple : 2023-12-24"),
    ] = False,
    last_update: Annotated[
        bool,
        typer.Option(
            "-u", help="Modifier la date du dernier contact - Exemple : 2023-12-24"
        ),
    ] = False,
):
    """Updates a given client."""
    token_check = clicollaborator._verify_token()
    if token_check:
        collaborator_department = token_check[1]["department_id"]
        collaborator_id = token_check[1]["collaborator_id"]
        try:
            client = Client.get(Client.id == client_id)

        except DoesNotExist:
            print(f"Aucun évènement trouvé avec l'ID n°{client_id}.")
            raise typer.Exit()

        if (
            int(collaborator_department) == SALES_DEPARTMENT_ID
            and int(collaborator_id) == client.collaborator.id
        ):
            if company:
                company_check = Company.get_or_none(Company.id == new_value)

                if company_check:
                    client.company = new_value
                    client.save()
                    print(
                        f"Le champ 'Entreprise' du client n°{client_id} a été mis à jour avec succès."
                    )

                else:
                    print("Veuillez entrer un numéro d'entreprise valide.")
                    raise typer.Exit(code=1)

            elif first_name:
                client.first_name = new_value
                client.save()
                print(
                    f"Le champ 'Prénom' du client n°{client_id} a été mis à jour avec succès."
                )

            elif name:
                client.name = new_value
                client.save()
                print(
                    f"Le champ 'Nom' du client n°{client_id} a été mis à jour avec succès."
                )

            elif email:
                client.email = new_value
                client.save()
                print(
                    f"Le champ 'Email' du client n°{client_id} a été mis à jour avec succès."
                )

            elif phone:
                client.phone = new_value
                client.save()
                print(
                    f"Le champ 'Téléphone' du client n°{client_id} a été mis à jour avec succès."
                )

            elif creation_date:
                client.creation_date = new_value
                client.save()
                print(
                    f"Le champ 'Date de création' du client n°{client_id} a été mis à jour avec succès."
                )

            elif last_update:
                client.last_update = new_value
                client.save()
                print(
                    f"Le champ 'Dernier contact' du client n°{client_id} a été mis à jour avec succès."
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
