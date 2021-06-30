import typer
from icon_cli.commands import config, tx

app = typer.Typer()

app.add_typer(config.app, name="config")
app.add_typer(tx.app, name="tx")
