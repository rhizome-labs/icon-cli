import typer

from icon_cli.commands import config, query

app = typer.Typer()

app.add_typer(config.app, name="config")
app.add_typer(query.app, name="query")
