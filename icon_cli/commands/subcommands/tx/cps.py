import typer

from icon_cli.config import Config
from icon_cli.dapps.cps import Cps
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
        "--keystore",
        "-k",
        callback=Validators.load_wallet_from_keystore,
    ),
):
    _cps = Cps(network)

    wallet_address = wallet.get_address()

    proposals = _cps.get_remaining_proposals_to_vote(wallet_address)
    progress_reports = _cps.get_remaining_progress_reports_to_vote(wallet_address)

    print(f"There are {len(proposals)} proposals and {len(progress_reports)} progress reports in your voting queue.")  # fmt: skip

    for proposal in proposals:
        print(f"\nProposal Title: {proposal['project_title']}")
        print(f"Requested Budget: {proposal['total_budget'] / 10**18} {proposal['token']}")  # fmt: skip
        vote = typer.prompt("Please type APPROVE (1), ABSTAIN (2), REJECT (3), or SKIP (4)")  # fmt: skip

        # Convert vote integer to string.
        vote = str(vote)

        if vote == "1":
            vote = "approve"
        elif vote == "2":
            vote = "abstain"
        elif vote == "3":
            vote = "reject"
        elif vote == "4":
            vote = "skip"
        else:
            vote = vote.lower()

        if vote not in ["approve", "abstain", "reject", "skip"]:
            die(f"{vote} is not a valid option. Valid options are APPROVE, ABSTAIN, REJECT, or SKIP.")  # fmt: skip
        if vote != "skip":
            reason = f"<p>{typer.prompt('Please provide a reason for your vote')}</p>"
            tx_hash = _cps.vote_proposal(
                wallet,
                f"_{vote}",
                reason,
                proposal["ipfs_hash"],
                0,
            )
            print(f"TX Hash: {tx_hash}")

    for progress_report in progress_reports:
        print(f"\nProgress Report Title: {progress_report['project_title']}")
        vote = typer.prompt("Please type APPROVE (1), ABSTAIN (2), REJECT (3), or SKIP (4)")  # fmt: skip

        # Convert vote integer to string.
        vote = str(vote)

        if vote == "1":
            vote = "approve"
        elif vote == "2":
            vote = "abstain"
        elif vote == "3":
            vote = "reject"
        elif vote == "4":
            vote = "skip"
        else:
            vote = vote.lower()

        if vote not in ["approve", "reject", "skip"]:
            die(f"{vote} is not a valid option. Valid options are APPROVE, REJECT, or SKIP.")  # fmt: skip
        if vote != "skip":
            reason = f"<p>{typer.prompt('Please provide a reason for your vote')}</p>"
            tx_hash = _cps.vote_progress_report(
                wallet,
                f"_{vote}",
                reason,
                progress_report["ipfs_hash"],
                progress_report["report_hash"],
                0,
            )
            print(f"TX Hash: {tx_hash}")
