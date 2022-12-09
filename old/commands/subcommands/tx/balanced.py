import typer
from icon_cli.config import Config
from icon_cli.dapps.balanced import Balanced
from icon_cli.utils import die
from icon_cli.validators import Validators

app = typer.Typer()


@app.command()
def peg_swap(
    value: str = typer.Argument(..., callback=Validators.validate_transaction_value),
    token: str = typer.Argument(..., callback=Validators.validate_token),
    network: str = typer.Option(
        Config.get_default_network(),
        "--network",
        "-n",
        callback=Validators.validate_network,
    ),
    wallet: str = typer.Option(
        Config.get_default_keystore(),
        "--keystore",
        "-k",
        callback=Validators.load_wallet_from_keystore,
    ),
):
    print("Hello!")
    _balanced = Balanced(network)
    tx_hash = _balanced.send_to_stability_fund(wallet, token, value)
    print(tx_hash)
