import typer
from icon_cli.callbacks import Callbacks
from icon_cli.config import Config
from icon_cli.icx import Icx, IcxNetwork
from icon_cli.utils import die, print_object
from rich import print

app = typer.Typer()


@app.command()
def debug():
    print_object(__name__)


@app.command()
def bond(
    address: str = typer.Option(..., "--address", "-a"),
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
    pass


@app.command()
def set_bonder_list(
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
    pass


@app.command()
def claim(
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
    icx = Icx(network)

    claimable_iscore = icx.query_claimable_iscore(keystore.get_address())

    if claimable_iscore["iscore"] < 1000:
        die("Sorry, minimum claim amount is 1,000 I-Score (1 ICX).")
    else:
        transaction = icx.build_call_transaction(
            keystore, icx.GOVERNANCE_CONTRACT, 0, "claimIScore"
        )
        transaction_result = icx.send_transaction(keystore, transaction)
        print(transaction_result)

