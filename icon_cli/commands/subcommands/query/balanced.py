import typer
from icon_cli.models.Balanced import Balanced
from icon_cli.models.Callbacks import Callbacks
from icon_cli.models.Config import Config
from icon_cli.utils import print_json
from rich import print

app = typer.Typer()


@app.command()
def debug():
    print(__name__)


@app.command()
def position(
    address: str = typer.Argument(..., callback=Callbacks.validate_icx_address),
    network: str = typer.Option(Config.get_default_network(), "--network", "-n", callback=Callbacks.validate_network),
    format: str = typer.Option(None, "--format", "-f", callback=Callbacks.validate_output_format),
):
    balanced = Balanced(network)
    position = balanced.query_position(address)

    if format == "json":
        print_json(position)
    else:
        print(position)
