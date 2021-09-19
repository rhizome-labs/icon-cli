import csv
import typer
from icon_cli.commands.subcommands.tx import balanced, gov
from icon_cli.callbacks import Callbacks
from icon_cli.config import Config
from icon_cli.icx import Icx, IcxNetwork
from icon_cli.utils import print_object
from rich import print

app = typer.Typer()

app.add_typer(balanced.app, name="balanced")
app.add_typer(gov.app, name="gov")


@app.command()
def debug():
    print_object(__name__)


@app.command()
def send(
    to: str = typer.Argument(..., callback=Callbacks.validate_icx_address),
    value: str = typer.Argument(..., callback=Callbacks.validate_transaction_value),
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
    simulation: bool = typer.Option(False, "--simulate", "-s"),
    confirmation: bool = typer.Option(True, "--confirm", "-c"),
    file: str = typer.Option(None, "--file", "-f")
):
    icx = Icx(network)

    transaction = icx.build_transaction(keystore, to, value)

    if simulation:
        print_object(transaction)
    else:
        if confirmation:
            prompt = typer.confirm("Please confirm transaction details.")
            if not prompt:
                print("Exiting now...")
                raise typer.Exit()
        transaction_result = icx.send_transaction(keystore, transaction)
        print(transaction_result)


# @app.command()
def send_batch(
    file: str = typer.Argument(...),
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
    simulation: bool = typer.Option(False, "--simulate", "-s"),
    confirmation: bool = typer.Option(True, "--confirm", "-c")
):
    icx = Icx(network)

    transactions = []

    if file is not None:

        with open(file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader, None)  # Skip headers.
            transactions = [icx.build_transaction(keystore, row[0], row[1]) for row in csv_reader]
            print(transactions)
