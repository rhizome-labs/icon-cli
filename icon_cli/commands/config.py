import typer
from icon_cli.models.Config import Config
from icon_cli.commands.subcommands.config import keystore
from rich import print

app = typer.Typer()

app.add_typer(keystore.app, name="keystore")


@app.command()
def debug():
    print(__name__)


@app.command()
def inspect():
    config = Config()
    print(config.inspect_config())
