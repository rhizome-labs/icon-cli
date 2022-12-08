import typer

from icon_cli.config import Config
from icon_cli.dapps.cps import Cps
from icon_cli.validators import Validators

app = typer.Typer()


@app.command()
def proposals(
    network: str = typer.Option(
        Config.get_default_network(),
        "--network",
        "-n",
        callback=Validators.validate_network,
    ),
):
    proposals = Cps(network).get_active_proposals()
    print(proposals)


@app.command()
def sponsor_bond(
    address: str = typer.Argument(
        ...,
        callback=Validators.validate_address,
    ),
    network: str = typer.Option(
        Config.get_default_network(),
        "--network",
        "-n",
        callback=Validators.validate_network,
    ),
):
    return
