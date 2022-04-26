import typer
from icon_cli.commands.subcommands.tx import cps

app = typer.Typer()

app.add_typer(cps.app, name="cps")
