import typer
from icon_cli.models.Config import Config
from icon_cli.commands.subcommands.config import keystore
from icon_cli.utils import print_json, print_object

app = typer.Typer()

app.add_typer(keystore.app, name="keystore")


@app.command()
def debug():
    print_object(__name__)


@app.command()
def inspect():
    print_json(Config.inspect_config())
