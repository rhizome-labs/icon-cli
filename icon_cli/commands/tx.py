import typer
from rich import print

from icon_cli.config import Config
from icon_cli.icx import Icx
from icon_cli.validators import Validators

app = typer.Typer()


@app.command()
def send(
    to_address: str = typer.Argument(
        ...,
        callback=Validators.validate_address,
    ),
    value: float = typer.Argument(...),
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
    icx = Icx(network, keystore_name, keystore_password)
    tx = icx.build_transaction(to_address, value)
    tx_hash = icx.send_transaction(tx)
    print(tx_hash)


@app.command()
def call(
    contract_address: str = typer.Argument(...),
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
    icx = Icx(network, keystore_name, keystore_password)
    abi = icx.get_score_api(contract_address)

    tx_methods = {}
    for method in abi:
        if method["type"] == "function" and "readonly" not in method.keys():
            tx_methods[method["name"]] = method

    method_names = sorted(list(tx_methods.keys()))

    method_choices = "\n".join(
        [f"{index}: {method}" for index, method in enumerate(method_names, start=1)]
    )

    print("\n")
    print(method_choices)
    print("\n")

    method_choice = typer.prompt(f"Enter the number of the method to call")

    return
