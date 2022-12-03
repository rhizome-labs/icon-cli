import typer
from icon_cli.commands.subcommands.tx import balanced, cps
from icon_cli.config import Config
from icon_cli.icx import Icx
from icon_cli.tokens import Tokens
from icon_cli.validators import Validators

app = typer.Typer()

app.add_typer(cps.app, name="cps")
app.add_typer(balanced.app, name="balanced")


@app.command()
def send(
    to: str = typer.Argument(..., callback=Validators.validate_address),
    value: str = typer.Argument(..., callback=Validators.validate_transaction_value),
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
    token: str = typer.Option(
        None, "--token", "-t", callback=Validators.validate_token
    ),
):
    _icx = Icx(network)
    if token is not None:  # Token transfer
        token_precision = Tokens.get_token_precision_from_contract(token)
        tx_hash = _icx.transfer_token(wallet, to, token, value, token_precision)
        print(tx_hash)
    else:  # ICX transfer
        tx_hash = _icx.build_transaction(wallet, to, value * 10**18)
        print(tx_hash)
