import typer
from icon_cli.commands import config, query, tx
from icon_cli.models.Config import Config

Config.initialize_config()
Config.ping()

app = typer.Typer()

app.add_typer(config.app, name="config")
app.add_typer(query.app, name="query")
app.add_typer(tx.app, name="tx")
