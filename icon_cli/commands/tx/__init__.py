import json

import typer
from rich import inspect, print

from icon_cli import CONFIG
from icon_cli.config import Config
from icon_cli.contracts import Contracts
from icon_cli.icx import IcxTx
from icon_cli.utils import Utils
from icon_cli.validators import Validators

app = typer.Typer(help="Build and send ICX transactions.")


@app.command()
def call(
    contract_address: str = typer.Argument(
        ...,
        callback=Validators.validate_contract_address,
    ),
    value: float = typer.Argument(0),
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
    build_only: bool = False,
):
    """
    Make a smart contract call.
    """
    # If contract address doesn't start with "cx", check if it's a known contract.
    if not contract_address.startswith("cx"):
        contract_address = Contracts.get_contract_address_from_name(
            contract_address, network
        )

    # Initialize IcxTx object.
    icx = IcxTx(network, keystore_name, keystore_password)

    # Load ABI for the contract.
    abi = icx.get_score_api(contract_address)

    # Create a dictionary that maps method name to its ABI.
    tx_methods = {}
    for method in abi:
        if method["type"] == "function" and "readonly" not in method.keys():
            tx_methods[method["name"]] = method

    # Create an alphabetical list of method names.
    method_names = sorted(list(tx_methods.keys()))

    # Create a numbered list of method names and join elements with a newline.
    method_choices = "\n".join(
        [f"{index}: {method}" for index, method in enumerate(method_names, start=1)]
    )

    # Ask user for the method to call.
    print(f"\nContract Address: {contract_address}\n")
    print(f"{method_choices}\n")
    method_choice = typer.prompt(f"Enter the number of the method to call")

    try:
        # Convert method choice to an integer.
        method_choice = int(method_choice)
        # Ensure method choice integer is within range.
        if method_choice < 1 or method_choice > len(method_names):
            raise ValueError
    except:
        Utils.exit("Please enter a valid number.", "error")

    method_to_call = method_names[method_choice - 1]
    method_to_call_abi = tx_methods[method_to_call]

    print("\n")
    print(method_to_call)
    print(json.dumps(method_to_call_abi, indent=4))
    print("\n")

    # Initialize dictionary to hold params for transaction.
    params = {}

    # Loop through inputs that require params.
    for param in method_to_call_abi["inputs"]:
        param_name = param["name"]
        param_type = param["type"]

        # Ask user to provide a value for the param.
        param_value = typer.prompt(f"Provide a value for {param_name} ({param_type})")

        # Do some type checking.
        if param_type == "Address":
            Validators.validate_address(param_value)
        elif param_type == "bool":
            param_value = bool(param_value)
        elif param_type == "int":
            param_value = int(param_value)
        elif param_type == "str":
            param_value = str(param_value)

        # Add param to the `params` dictionary.
        params[param_name] = param_value

    # Build transaction.
    tx = icx.build_call_transaction(
        contract_address,
        int(value * 10**18),
        method_to_call,
        params,
    )

    # Confirm transaction.
    inspect(tx)
    tx_confirmation = typer.confirm("Please confirm the transaction details")

    # Proceed if user gives confirmation.
    if tx_confirmation:

        # Return tx object if build_only is True.
        if build_only is True:
            return tx

        # Send transaction.
        tx_hash = icx.send_transaction(tx)
        print(tx_hash)


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
    build_only: bool = False,
):
    """
    Send an ICX transaction.
    """
    icx = IcxTx(network, keystore_name, keystore_password)
    tx = icx.build_transaction(to_address, value)

    # Return tx object if build_only is True.
    if build_only is True:
        return tx

    tx_hash = icx.send_transaction(tx)
    print(tx_hash)
