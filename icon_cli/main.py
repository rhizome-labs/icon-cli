import typer

from icon_cli.commands import config

app = typer.Typer()

app.add_typer(config.app, name="config")


@app.command()
def hello():
    print("HELLO!")
