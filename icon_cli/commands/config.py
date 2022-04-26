import typer
from icon_cli.config import Config
from rich import inspect, print

app = typer.Typer()


@app.command()
def debug():
    inspect(__name__)


@app.command()
def inspect():
    config = Config.inspect_config()
    print(config)
