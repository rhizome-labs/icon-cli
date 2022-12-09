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
    keystore_name: str = typer.Option(
        Config.get_default_keystore(),
        "--keystore",
        "-k",
    ),
    keystore_password: str = typer.Option(
        None,
        "--password",
        "-p",
    ),
):
    keystore = Icx.load_keystore(keystore_name, keystore_password)
    icx = Icx(network)
    tx = icx.build_transaction(to, amount, keystore)
    tx_hash = icx.send_transaction(tx, keystore)
    print(tx_hash)
