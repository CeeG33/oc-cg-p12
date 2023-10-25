import os, jwt, typer
from rich import print
from rich.console import Console
from rich.table import Table
from typing_extensions import Annotated
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from peewee import DoesNotExist
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from dotenv import load_dotenv, set_key, get_key
from epicevents.sentry import sentry_sdk
from epicevents.data_access_layer.collaborator import Collaborator
from epicevents.data_access_layer.department import Department

dotenv_file = load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
if os.getenv("TOKEN"):
    TOKEN = os.getenv("TOKEN")

MANAGEMENT_DEPARTMENT_ID = 1
SALES_DEPARTMENT_ID = 2
SUPPORT_DEPARTMENT_ID = 3

app = typer.Typer()

ph = PasswordHasher()


def _generate_token(collaborator):
    token = jwt.encode(collaborator.get_data(), key=SECRET_KEY, algorithm="HS256")
    return token


def _memorize_token(token):
    set_key(".env", "TOKEN", token)


def _read_token():
    return get_key(".env", "TOKEN")


def _verify_token():
    try:
        decoded_payload = jwt.decode(
            _read_token(), key=SECRET_KEY, algorithms=["HS256"]
        )
    except ExpiredSignatureError:
        print("Token expiré, veuillez vous réauthentifier.")
        raise ExpiredSignatureError

    collaborator_id = decoded_payload.get("collaborator_id")

    if collaborator_id is None or not isinstance(int(collaborator_id), int):
        print("Le token n'est pas valide, veuillez vous réauthentifier.")
        raise InvalidTokenError

    return True, decoded_payload


def _create_collaborators_table():
    table = Table(title="Tableau des collaborateurs")
    table.add_column("[ID]", justify="center", no_wrap=True, style="cyan")
    table.add_column("[Prénom]", justify="center", no_wrap=True, style="orange_red1")
    table.add_column("[Nom]", justify="center", no_wrap=True, style="orange_red1")
    table.add_column("[Email]", justify="center", no_wrap=True, style="yellow")
    table.add_column(
        "[Departement]", justify="center", no_wrap=True, style="chartreuse4"
    )

    return table


def _add_rows_in_collaborators_table(user, table):
    table.add_row(
        f"{user.id}",
        f"{user.first_name}",
        f"{user.name}",
        f"{user.email}",
        f"{user.department.name}",
    )


def _print_table(queryset):
    table = _create_collaborators_table()

    for user in queryset:
        _add_rows_in_collaborators_table(user, table)

    console = Console()
    console.print(table)


@app.command()
def login(
    email: Annotated[
        str,
        typer.Option(
            prompt=True, help="Email du collaborateur - Exemple : exemple@email.com"
        ),
    ],
    password: Annotated[
        str,
        typer.Option(
            prompt=True, help="Mot de passe", confirmation_prompt=True, hide_input=True
        ),
    ],
):
    """Logs into the software."""
    collaborator = Collaborator.get_or_none(Collaborator.email == email)

    if collaborator:
        if hasattr(collaborator, "password"):
            try:
                password_check = ph.verify(collaborator.password, password)
            except VerifyMismatchError:
                print("Nom d'utilisateur ou mot de passe incorrect.")
                raise typer.Exit(code=1)

    if not collaborator:
        print("Nom d'utilisateur ou mot de passe incorrect.")
        raise typer.Exit(code=1)

    print("Authentification réussie.")
    token = _generate_token(collaborator)
    _memorize_token(token)


@app.command()
def list():
    """Lists all collaborators."""
    token_check = _verify_token()

    if token_check:
        collaborator_department = token_check[1]["department_id"]

        if int(collaborator_department) == MANAGEMENT_DEPARTMENT_ID:
            queryset = Collaborator.select()

            if len(queryset) == 0:
                print("La base de donnée ne contient aucun collaborateur.")
                raise typer.Exit()

            _print_table(queryset)

        else:
            print("Action restreinte.")
            raise typer.Exit()

    else:
        print("Veuillez vous authentifier et réessayer.")
        raise typer.Exit()


@app.command()
def create(
    first_name: Annotated[
        str,
        typer.Option(prompt="Prénom", help="Prénom du collaborateur - Exemple : Alain"),
    ],
    name: Annotated[
        str, typer.Option(prompt="Nom", help="Nom du collaborateur - Exemple : Terieur")
    ],
    password: Annotated[
        str,
        typer.Option(
            prompt="Mot de passe",
            help="Mot de passe du collaborateur",
            confirmation_prompt=True,
            hide_input=True,
        ),
    ],
    email: Annotated[
        str,
        typer.Option(
            prompt="Email",
            help="Adresse mail du collaborateur - Exemple : alain.terieur@mail.com",
        ),
    ],
    department: Annotated[
        int,
        typer.Option(
            prompt="N° de département",
            help="Numéro de département du collaborateur - Rappel : 1 > Gestion - 2 > Commercial - 3 > Support",
        ),
    ],
):
    """Creates a new collaborator."""
    token_check = _verify_token()
    if token_check:
        collaborator_department = token_check[1]["department_id"]
        collaborator_id = token_check[1]["collaborator_id"]

        if int(collaborator_department) == MANAGEMENT_DEPARTMENT_ID:
            Collaborator.create(
                first_name=first_name,
                name=name,
                email=email,
                password=password,
                department=department,
            )
            print(f"Le collaborateur {first_name} {name} a été créé avec succès.")
            sentry_sdk.capture_message(
                f"[CREATION COLLABORATEUR PAR COLLABORATEUR N°{collaborator_id}] >> Prénom : {first_name} - Nom : {name} - Email : {email} - Département : {department}"
            )

        else:
            print("Action restreinte.")
            raise typer.Exit()

    else:
        print("Veuillez vous authentifier et réessayer.")
        raise typer.Exit()


@app.command()
def update(
    collaborator_id: Annotated[
        int, typer.Argument(help="N° du collaborateur à modifier - Exemple : 1")
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
    password: Annotated[
        bool, typer.Option("-p", help="Modifier le mot de passe")
    ] = False,
    department: Annotated[
        bool, typer.Option("-d", help="Modifier le département - Exemple : 1")
    ] = False,
):
    """Updates a given collaborator."""
    token_check = _verify_token()
    if token_check:
        collaborator_department = token_check[1]["department_id"]
        user_id = token_check[1]["collaborator_id"]

        if int(collaborator_department) == MANAGEMENT_DEPARTMENT_ID:
            try:
                collaborator = Collaborator.get(Collaborator.id == collaborator_id)

                if first_name:
                    collaborator.first_name = new_value
                    collaborator.save()
                    print(
                        f"Le champ 'Prénom' du collaborateur n°{collaborator_id} a été mis à jour avec succès."
                    )
                    sentry_sdk.capture_message(
                        f"[MAJ COLLABORATEUR N°{collaborator_id} PAR COLLABORATEUR N°{user_id}] >> Prénom : {new_value}"
                    )

                elif name:
                    collaborator.name = new_value
                    collaborator.save()
                    print(
                        f"Le champ 'Nom' du collaborateur n°{collaborator_id} a été mis à jour avec succès."
                    )
                    sentry_sdk.capture_message(
                        f"[MAJ COLLABORATEUR N°{collaborator_id} PAR COLLABORATEUR N°{user_id}] >> Nom : {new_value}"
                    )

                elif email:
                    collaborator.email = new_value
                    collaborator.save()
                    print(
                        f"Le champ 'Email' du collaborateur n°{collaborator_id} a été mis à jour avec succès."
                    )
                    sentry_sdk.capture_message(
                        f"[MAJ COLLABORATEUR N°{collaborator_id} PAR COLLABORATEUR N°{user_id}] >> Email : {new_value}"
                    )

                elif password:
                    collaborator.password = new_value
                    collaborator.save()
                    print(
                        f"Le champ 'Mot de passe' du collaborateur n°{collaborator_id} a été mis à jour avec succès."
                    )
                    sentry_sdk.capture_message(
                        f"[MAJ COLLABORATEUR N°{collaborator_id} PAR COLLABORATEUR N°{user_id}] >> Nouveau mot de passe"
                    )

                elif department:
                    department_check = Department.get_or_none(
                        Department.id == new_value
                    )

                    if department_check:
                        collaborator.department = new_value
                        collaborator.save()
                        print(
                            f"Le champ 'Département' du collaborateur n°{collaborator_id} a été mis à jour avec succès."
                        )
                        sentry_sdk.capture_message(
                            f"[MAJ COLLABORATEUR N°{collaborator_id} PAR COLLABORATEUR N°{user_id}] >> Département : {new_value}"
                        )

                    else:
                        print("Veuillez entrer un numéro de département valide.")
                        raise typer.Exit(code=1)

                else:
                    print("Vous n'avez pas sélectionné d'attribut à modifier.")
                    raise typer.Exit()

            except DoesNotExist:
                print(f"Aucun collaborateur trouvé avec l'ID n°{collaborator_id}.")

        else:
            print("Action restreinte.")
            raise typer.Exit()

    else:
        print("Veuillez vous authentifier et réessayer.")
        raise typer.Exit()


@app.command()
def delete(
    collaborator_id: Annotated[
        int,
        typer.Option(
            prompt="N° du collaborateur",
            confirmation_prompt=True,
            help="Numéro du collaborateur",
        ),
    ]
):
    """Deletes a collaborator."""
    token_check = _verify_token()
    if token_check:
        collaborator_department = token_check[1]["department_id"]
        user_id = token_check[1]["collaborator_id"]

        if int(collaborator_department) == MANAGEMENT_DEPARTMENT_ID:
            try:
                collaborator = Collaborator.get(Collaborator.id == collaborator_id)
                collaborator.delete_instance()
                print(
                    f"Le collaborateur n°{collaborator_id} a été supprimé avec succès."
                )
                sentry_sdk.capture_message(
                    f"[SUPPRESSION COLLABORATEUR N°{collaborator_id} PAR COLLABORATEUR N°{user_id}]"
                )

            except DoesNotExist:
                print(f"Aucun collaborateur trouvé avec l'ID n°{collaborator_id}.")

        else:
            print("Action restreinte.")
            raise typer.Exit()

    else:
        print("Veuillez vous authentifier et réessayer.")
        raise typer.Exit()


if __name__ == "__main__":
    app()
