import typer

from icon_cli.config import Config
from icon_cli.icx import Icx
from icon_cli.validators import Validators

app = typer.Typer()


@app.command()
def send(
    amount: float = typer.Argument(...),
    to: str = typer.Argument(
        ...,
        callback=Validators.validate_address,
    ),
    network: str = typer.Option(
        Config.get_default_network(),
        "--network",
        "-n",
        callback=Validators.validate_network,
    ),
    keystore: str = typer.Option(
        Config.get_default_keystore(),
        "--keystore",
        "-k",
        callback=Icx.load_keystore,
    ),
):
    icx = Icx(network)
    tx = icx.build_transaction(to, amount, keystore)
    tx_hash = icx.send_transaction(tx, keystore)
    print(tx_hash)
