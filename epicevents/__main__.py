import typer
import sentry_sdk
from rich import print
from .cli.client import app as app_client
from .cli.collaborator import app as app_collaborator
from .cli.contract import app as app_contract
from .cli.event import app as app_event

app = typer.Typer()

app.add_typer(app_collaborator, name="collaborators", help="Manages collaborators.")
app.add_typer(app_client, name="clients", help="Manages clients.")
app.add_typer(app_contract, name="contracts", help="Manages contracts.")
app.add_typer(app_event, name="events", help="Manages events.")

if __name__ == "__main__":
    try:
        app()
    except Exception as e:
        print(e)
        sentry_sdk.capture_exception(e)
