import typer
from icon_cli.models.Config import Config
from icon_cli.models.Icx import Icx
from icon_cli.models.Identity import Identity
from icon_cli.utils import print_json
from rich import print

app = typer.Typer()

config = Config()
identity = Identity()


@app.command()
def debug():
    print(__name__)


@app.command()
def build(
    to: str = typer.Argument(...),
    value: int = typer.Argument(...),
    keystore: str = typer.Option(config.get_default_keystore(), "--keystore", "-k"),
    network: str = typer.Option(config.get_default_network(), "--network", "-n"),
):
    icx = Icx(network)
    wallet = identity.load_wallet(keystore)
    transaction = icx.build_transaction(wallet, to, value)
    print_json(transaction.__dict__)
