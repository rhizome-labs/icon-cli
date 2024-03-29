import typer
from rich import print

from icon_cli.config import Config
from icon_cli.icx import IcxQuery
from icon_cli.tracker import Tracker

app = typer.Typer(help="Query a node on the ICON network.")
from icon_cli.validators import Validators


@app.command()
def abi(
    contract_address: str = typer.Argument(
        ...,
        callback=Validators.validate_contract_address,
        help="An ICON contract address.",
    ),
    network: str = typer.Option(
        Config.get_default_network(),
        "--network",
        "-n",
        help="The name of the ICON network to use.",
    ),
):
    """
    View the ABI of an ICON SCORE.
    """
    icx = IcxQuery(network)
    abi = icx.get_score_api(contract_address)
    print(abi)


@app.command()
def balance(
    address: str = typer.Argument(
        Config.get_default_keystore_address(),
        help="An ICON wallet address.",
        show_default=False,
    ),
    network: str = typer.Option(
        Config.get_default_network(),
        "--network",
        "-n",
        help="The name of the ICON network to use.",
        show_default=False,
    ),
    in_loop: bool = typer.Option(
        False,
        help="Display the output value in loop.",
        show_default=False,
    ),
    token_symbol: str = typer.Option(
        None, "--token", "-t", help="An IRC-2 token symbol."
    ),
):
    """
    View balance details for an ICX address.
    """
    icx = IcxQuery(network)
    if token_symbol is None:
        balance = icx.get_balance(address, in_loop=in_loop)
        print(f"{balance} ICX")
    else:
        balance = icx.get_token_balance(address, token_symbol, network)
        print(balance)


@app.command()
def block(
    block_height: int = typer.Argument(
        -1,
        help="A block number on the ICON blockchain.",
    ),
    network: str = typer.Option(
        Config.get_default_network(),
        "--network",
        "-n",
        help="The name of the ICON network to use.",
    ),
):
    """
    View details about an ICON block.
    """
    icx = IcxQuery(network)
    block = icx.get_block(block_height)
    print(block)


@app.command()
def tx(
    tx_hash: str = typer.Argument(
        ...,
        help="An ICX transaction hash.",
    ),
    network: str = typer.Option(
        Config.get_default_network(),
        "--network",
        "-n",
        help="The name of the ICON network to use.",
    ),
):
    """
    View details about an ICX transaction.
    """
    icx = IcxQuery(network)
    tx = icx.get_transaction(tx_hash)
    print(tx)


@app.command()
def tx_result(
    tx_hash: str = typer.Argument(
        ...,
        help="An ICX transaction hash.",
    ),
    network: str = typer.Option(
        Config.get_default_network(),
        "--network",
        "-n",
        help="The name of the ICON network to use.",
    ),
):
    """
    View details about the result of an ICX transaction.
    """
    icx = IcxQuery(network)
    tx_result = icx.get_transaction_result(tx_hash)
    print(tx_result)
