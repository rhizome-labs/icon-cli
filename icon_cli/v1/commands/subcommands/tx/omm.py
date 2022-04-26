import typer
from icon_cli.callbacks import Callbacks
from icon_cli.config import Config
from icon_cli.dapps.omm.Omm import Omm
from icon_cli.icx import Icx, IcxNetwork
from icon_cli.tokens import Tokens
from icon_cli.utils import die, print_object
from rich import print

app = typer.Typer()


@app.command()
def debug():
    print_object(__name__)


@app.command()
def update_delegation(
    prep_address: str = typer.Argument(..., callback=Callbacks.validate_icx_address),
    keystore: str = typer.Option(
        Config.get_default_keystore(),
        "--keystore",
        "-k",
        callback=Callbacks.load_wallet_from_keystore,
    ),
    network: IcxNetwork = typer.Option(
        Config.get_default_network(),
        "--network",
        "-n",
        callback=Callbacks.enforce_mainnet,
        case_sensitive=False,
    ),
):
    omm = Omm(network)
    transaction_result = omm.update_delegation(keystore, prep_address)
    print(transaction_result)
