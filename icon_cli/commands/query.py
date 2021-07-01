import typer
from icon_cli.commands.subcommands.query import balanced
from rich import print

app = typer.Typer()

app.add_typer(balanced.app, name="balanced")


@app.command()
def debug():
    print(__name__)
