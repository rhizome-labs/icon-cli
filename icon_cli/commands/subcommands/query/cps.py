import typer
from concurrent.futures import ThreadPoolExecutor
from icon_cli.dapps.cps.Cps import Cps
from icon_cli.callbacks import Callbacks
from icon_cli.config import Config
from icon_cli.icx import IcxNetwork
from icon_cli.models.Prep import Prep
from icon_cli.utils import (
    format_number_display,
    kv_table,
    print_json,
    print_object,
    print_table
)
from rich import box
from rich import print
from rich.table import Table

app = typer.Typer()


@app.command()
def debug():
    print_object(__name__)


@app.command()
def balance(
    network: IcxNetwork = typer.Option(
        Config.get_default_network(),
        "--network",
        "-n",
        callback=Callbacks.enforce_mainnet,
        case_sensitive=False,
    ),
    format: str = typer.Option(None, "--format", "-f", callback=Callbacks.validate_output_format),
):
    """
    Returns the amount of ICX in the CPS treasury.
    """
    cps = Cps(network)
    balance = cps.query_cps_balance()

    if format == "json":
        response = {"cps_icx_balance": format_number_display(balance, 0, 18)}
        print_json(response)
    else:
        print(f"CPS Balance: {format_number_display(balance, 0, 4)} ICX")


@app.command()
def period(
    network: IcxNetwork = typer.Option(
        Config.get_default_network(),
        "--network",
        "-n",
        callback=Callbacks.enforce_mainnet,
        case_sensitive=False,
    ),
    format: str = typer.Option(None, "--format", "-f", callback=Callbacks.validate_output_format),
):
    cps = Cps(network)
    period_status = cps.query_period_status()

    if format == "json":
        print_json(period_status)
    else:
        rows = [
            ["Current Block", format_number_display(period_status["current_block"], 0, 0)],
            ["Next Block", format_number_display(period_status["next_block"], 0, 0)],
            ["Remaining Time", format_number_display(period_status["remaining_time"], 0, 0)],
            ["Period Name", period_status["period_name"]],
            ["Previous Period Name", period_status["previous_period_name"]],
            ["Period Span", format_number_display(period_status["period_span"], 0, 0)],
        ]
        kv_table(rows, "CPS Period Status")


@app.command()
def preps(
    network: IcxNetwork = typer.Option(
        Config.get_default_network(),
        "--network",
        "-n",
        callback=Callbacks.enforce_mainnet,
        case_sensitive=False,
    ),
    format: str = typer.Option(None, "--format", "-f", callback=Callbacks.validate_output_format),
):
    cps = Cps(network)
    preps = cps.query_cps_preps()

    if format == "json":
        print_json(preps)
    else:
        table = Table(box=box.MINIMAL, show_header=True, show_lines=True)
        for header in ["#", "NAME", "ADDRESS", "DELEGATION"]:
            table.add_column(header, justify="left")
        for prep in preps:
            table.add_row(
                str(preps.index(prep) + 1),
                prep["name"],
                prep["address"],
                f"{format_number_display(prep['delegated'], 0, 0)} ICX",
            )  # noqa 503
        print_table(table)


@app.command()
def proposal(
    address: str = typer.Argument(..., callback=Callbacks.validate_icx_address),
    network: IcxNetwork = typer.Option(
        Config.get_default_network(),
        "--network",
        "-n",
        callback=Callbacks.enforce_mainnet,
        case_sensitive=False,
    ),
    format: str = typer.Option(None, "--format", "-f", callback=Callbacks.validate_output_format),
):
    cps = Cps(network)
    proposal_details = cps.query_proposal_details(address)

    if format == "json":
        print_json(proposal_details)
    else:
        print(proposal_details)


@app.command()
def active_proposals(
    network: IcxNetwork = typer.Option(
        Config.get_default_network(),
        "--network",
        "-n",
        callback=Callbacks.enforce_mainnet,
        case_sensitive=False,
    ),
    format: str = typer.Option(None, "--format", "-f", callback=Callbacks.validate_output_format),
):
    cps = Cps(network)
    contributor_addresses = cps.query_cps_contributors()

    with ThreadPoolExecutor() as executor:
        all_proposals = list(executor.map(cps.query_proposal_details, contributor_addresses))

    active_proposals = []

    for proposal_set in all_proposals:
        for proposal in proposal_set:
            if proposal["status"] == "_active":
                active_proposals.append(proposal)

    if format == "json":
        print_json(active_proposals)
    else:
        table = Table(
            box=box.DOUBLE,
            show_lines=True,
            show_header=True,
            title="Active CPS Proposals",
            title_justify="left",
            title_style="bold",
        )

        for header in ["Sponsor", "Project Name", "IPFS Hash"]:
            table.add_column(header, justify="left")

        for proposal in active_proposals:
            sponsor_name = Prep.convert_address_to_name(proposal["sponsor_address"])
            project_title = proposal["project_title"]
            ipfs_hash = proposal["ipfs_hash"]
            table.add_row(sponsor_name, project_title, ipfs_hash)

        print_table(table)
