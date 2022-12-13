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


@app.command()
def vote(
    proposal_id: str = typer.Argument(
        ...,
        help="Transaction hash for a network proposal.",
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
    """
    Cast a vote on an ICON network proposal.
    """
    icx = IcxTx(network, keystore_name, keystore_password)
    try:
        proposal_details = icx.call(
            Contracts.get_contract_address_from_name("governance", network),
            "getProposal",
            {"id": proposal_id},
        )
    except:
        Utils.exit(f"{proposal_id} is not a valid network proposal.")

    print(f"Title: {proposal_details['contents']['title']}")
    print(f"Description: {proposal_details['contents']['title']}")
    print(f"Proposed By: {proposal_details['proposerName']} ({proposal_details['proposer']})")  # fmt: skip

    vote_decision = typer.confirm("Would you like to approve this network proposal?")  # fmt: skip

    if vote_decision is True:
        vote_confirmation = typer.confirm("Please confirm that you'd like to APPROVE this network proposal.")  # fmt: skip
        if vote_confirmation:
            vote = 1
    else:
        vote_confirmation = typer.confirm("Please confirm that you'd like to REJECT this network proposal.")  # fmt: skip
        if vote_confirmation:
            vote = 0

    tx = icx.build_call_transaction(
        Contracts.get_contract_address_from_name("governance", network),
        method="voteProposal",
        params={"id": proposal_id, "vote": vote},
    )
    tx_hash = icx.send_transaction(tx)

    print(tx_hash)
