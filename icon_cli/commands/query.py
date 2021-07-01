import typer
from icon_cli.commands.subcommands.query import balanced, gov
from icon_cli.models.Callbacks import Callbacks
from icon_cli.models.Config import Config
from icon_cli.models.Icx import Icx
from icon_cli.utils import print_json
from rich import print

app = typer.Typer()

app.add_typer(balanced.app, name="balanced")
app.add_typer(gov.app, name="gov")


@app.command()
def debug():
    print(__name__)


@app.command()
def block(
    block: int = typer.Argument(0, callback=Callbacks.validate_block),
    network: str = typer.Option(Config.get_default_network(), "--network", "-n"),
    format: str = typer.Option(None, "--format", "-f", callback=Callbacks.validate_output_format),
):
    """
    Returns block info for the specified block height.
    """
    icx = Icx(network)
    block_data = icx.query_block(block)

    if format == "json":
        print_json(block_data)
    else:
        print("TBD")
