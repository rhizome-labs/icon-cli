import typer
from icon_cli.callbacks import Callbacks
from icon_cli.config import Config
from icon_cli.dapps.omm.Omm import Omm
from icon_cli.icx import IcxNetwork
from icon_cli.prep import Prep
from icon_cli.utils import format_number_display, print_json, print_object, print_table
from rich import box, print
from rich.table import Table

app = typer.Typer()

callbacks = Callbacks()


@app.command()
def debug():
    print_object(__name__)


@app.command()
def stake(
    address: str = typer.Argument(..., callback=Callbacks.validate_icx_address),
    network: IcxNetwork = typer.Option(
        Config.get_default_network(),
        "--network",
        "-n",
        callback=Callbacks.enforce_mainnet,
        case_sensitive=False,
    ),
):
    _omm = Omm(network)
    omm_stake = _omm.get_omm_stake(address)
    print(f"{omm_stake / 10 ** 18} OMM")
