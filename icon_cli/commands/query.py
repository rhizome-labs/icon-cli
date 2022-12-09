from typing import Union

import typer
from rich import print

from icon_cli.config import Config
from icon_cli.icx import Icx
from icon_cli.utils import Utils

app = typer.Typer()


@app.command()
def abi(
    contract_address: str = typer.Argument(
        ...,
        callback=Utils.validate_address,
    ),
    network: str = Config.get_config_default_network(),
):
    icx = Icx(network)
    abi = icx.get_score_api(contract_address)
    print(abi)


@app.command()
def block(
    block_height: int = typer.Argument(-1),
    network: str = Config.get_config_default_network(),
):
    icx = Icx(network)
    block = icx.get_block(block_height)
    print(block)


@app.command()
def tx(
    tx_hash: str = typer.Argument(...),
    network: str = Config.get_config_default_network(),
):
    icx = Icx(network)
    tx = icx.get_transaction(tx_hash)
    print(tx)


@app.command()
def tx_result(
    tx_hash: str = typer.Argument(...),
    network: str = Config.get_config_default_network(),
):
    icx = Icx(network)
    tx_result = icx.get_transaction_result(tx_hash)
    print(tx_result)
