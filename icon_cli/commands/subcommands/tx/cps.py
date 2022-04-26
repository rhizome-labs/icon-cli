from time import sleep

import typer
from icon_cli.config import Config
from icon_cli.dapps.cps.cps import Cps
from icon_cli.utils import die
from icon_cli.validators import Validators

app = typer.Typer()


@app.command()
def vote(
    network: str = typer.Option(
        Config.get_default_network(),
        "--network",
        "-n",
        callback=Validators.validate_network,
    ),
    wallet: str = typer.Option(
        Config.get_default_keystore(),
        "--wallet",
        "-w",
        callback=Validators.load_wallet_from_keystore,
    ),
):
    _cps = Cps(network)
    proposals = _cps.get_remaining_proposals_to_vote(wallet.get_address())
    progress_reports = _cps.get_remaining_progress_reports_to_vote(wallet.get_address())

    print(
        f"There are {len(proposals)} proposals and {len(progress_reports)} progress reports in your voting queue."
    )

    for proposal in proposals:
        print(f"\nProposal Title: {proposal['project_title']}")
        print(
            f"Requested Budget: {proposal['total_budget'] / 10**18} {proposal['token']}"
        )
        vote = typer.prompt("Please type APPROVE, ABSTAIN, REJECT, or SKIP")
        vote = vote.lower()
        if vote not in ["approve", "abstain", "reject", "skip"]:
            die(
                f"{vote} is not a valid option. Valid options are APPROVE, ABSTAIN, REJECT, or SKIP."
            )
        if vote != "skip":
            reason = f"<p>{typer.prompt('Please provide a reason for your vote')}</p>"
            tx_hash = _cps.vote_proposal(
                wallet, f"_{vote}", reason, proposal["ipfs_hash"], 0
            )
            print(f"TX Hash: {tx_hash}")
