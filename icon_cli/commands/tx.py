import typer
from icon_cli.models.Callbacks import Callbacks
from icon_cli.models.Config import Config
from icon_cli.models.Icx import Icx

app = typer.Typer()

callbacks = Callbacks()
config = Config()


@app.command()
def debug():
    typer.echo(__name__)


@app.command()
def send(
    to: str = typer.Argument(...),
    value: str = typer.Argument(...),
    wallet: str = typer.Option(
        config.get_default_keystore(), "--keystore", "-k", callback=callbacks.convert_keystore_to_wallet
    ),
    network: str = typer.Option(config.get_default_network(), "--network", "-in"),
):
    icx = Icx(network)
    transaction = icx.build_transaction(wallet, to, value)
    # print(transaction)
