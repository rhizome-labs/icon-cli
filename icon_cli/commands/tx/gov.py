import os
import shutil
from datetime import datetime
from pathlib import Path

import typer
from rich import print

from icon_cli.config import Config
from icon_cli.contracts import Contracts
from icon_cli.icx import IcxTx
from icon_cli.utils import Utils
from icon_cli.validators import Validators

app = typer.Typer(help="Govern the ICON blockchain.")


@app.command()
def claim_iscore(
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
    """
    Claim ICX staking rewards.
    """
    icx = IcxTx(network, keystore_name, keystore_password)
    tx = icx.build_call_transaction(
        Contracts.get_contract_address_from_name("chain", network), method="claimIScore"
    )
    tx_hash = icx.send_transaction(tx)
    print(tx_hash)
