from datetime import datetime

import typer
from icon_cli.callbacks import Callbacks
from icon_cli.config import Config
from icon_cli.dapps.balanced.BalancedDividends import BalancedDividends
from icon_cli.dapps.balanced.BalancedLoans import BalancedLoans
from icon_cli.icx import IcxNetwork
from icon_cli.utils import (
    format_number_display,
    hex_to_int,
    print_json,
    print_object,
    print_table,
)
from rich import box, print
from rich.console import Console
from rich.table import Table

app = typer.Typer()


@app.command()
def debug():
    print_object(__name__)


@app.command()
def position(
    address: str = typer.Argument(..., callback=Callbacks.validate_icx_address),
    network: IcxNetwork = typer.Option(
        Config.get_default_network(),
        "--network",
        "-n",
        callback=Callbacks.enforce_mainnet,
        case_sensitive=False,
    ),
    format: str = typer.Option(
        None, "--format", "-f", callback=Callbacks.validate_output_format
    ),
):
    balanced_loans = BalancedLoans(network)

    position = balanced_loans.query_position_from_address(address)

    if format == "json":
        print_json(position)
    else:
        table = Table(
            box=box.DOUBLE,
            show_lines=True,
            show_header=False,
            title="Balanced Position Details",
            title_justify="left",
            title_style="bold",
        )

        table.add_column("Key", justify="left", style="bold")
        table.add_column("Value", justify="left")

        created_at = (
            datetime.fromtimestamp(position["created"] / 1000000)
            .astimezone()
            .replace(microsecond=0)
            .isoformat()
        )

        assets = [
            f"{format_number_display(amount, 0, 4)} {ticker}"
            for ticker, amount in position["assets"].items()
        ]

        table.add_row("ADDRESS", position["address"])
        table.add_row("STANDING", position["standing"])
        table.add_row("POSITION ID", format_number_display(position["pos_id"], 0, 0))
        table.add_row("CREATED", str(created_at))
        table.add_row("RATIO", format_number_display(position["ratio"]))
        table.add_row("TOTAL_DEBT", format_number_display(position["total_debt"]))
        table.add_row("COLLATERAL", format_number_display(position["collateral"]))
        table.add_row("ASSETS", ", ".join(assets))
        table.add_row("SNAPSHOT ID", str(position["snap_id"]))
        table.add_row("SNAPSHOT LENGTH", str(position["snaps_length"]))
        table.add_row("FIRST DAY", str(position["first day"]))

        print_table(table)


@app.command()
def position_count(
    network: IcxNetwork = typer.Option(
        Config.get_default_network(),
        "--network",
        "-n",
        callback=Callbacks.enforce_mainnet,
        case_sensitive=False,
    ),
    format: str = typer.Option(
        None, "--format", "-f", callback=Callbacks.validate_output_format
    ),
):
    balanced_loans = BalancedLoans(network)

    position_count = balanced_loans.query_position_count()

    if format == "json":
        response = {"position_count": position_count}
        print_json(response)
    else:
        print(f"Balanced Position Count: {position_count}")


@app.command()
def positions(
    index_start: int = typer.Option(1, "--start", "-s"),
    index_end: int = typer.Option(None, "--end", "-e"),
    min_collateralization: int = typer.Option(150, "--min-collateralization", "-min"),
    max_collateralization: int = typer.Option(300, "--max-collateralization", "-max"),
    sort_key: str = typer.Option(None, "--sort", "-k"),
    reverse: bool = typer.Option(False, "--reverse", "-r"),
    network: IcxNetwork = typer.Option(
        Config.get_default_network(),
        "--network",
        "-n",
        callback=Callbacks.enforce_mainnet,
        case_sensitive=False,
    ),
    format: str = typer.Option(
        None, "--format", "-f", callback=Callbacks.validate_output_format
    ),
):
    balanced_loans = BalancedLoans(network)
    console = Console()

    # If index_end is None, set index_end to maximum.
    if not index_end:
        index_end = balanced_loans.query_position_count() + 1

    # If sort_key is None, set sort_key to "pos_id".
    if not sort_key:
        sort_key = "pos_id"

    with console.status("[bold green]Querying Balanced positions..."):
        positions = balanced_loans.query_positions(
            index_start,
            index_end,
            min_collateralization,
            max_collateralization,
            sort_key,
            reverse,
        )

    # Raise error if there are no Balanced positions.
    if len(positions) == 0:
        print("There are no Balanced positions that fit these parameters.")
        raise typer.Exit()

    if format == "json":
        print_json(positions)
    else:
        table = Table(box=box.MINIMAL, show_header=True, show_lines=True)

        for header in ["#", "ADDRESS", "DEBT", "COLLATERAL", "COLLAT %"]:
            table.add_column(header, justify="left")

        for position in positions:
            table.add_row(
                str(position["pos_id"]),  # "#" # noqa 503
                position["address"],  # ADDRESS # noqa 503
                f"{format_number_display(position['total_debt'], 0, 2)} bnUSD",  # DEBT # noqa 503
                f"{format_number_display(position['collateral'], 0, 2)} sICX",  # COLLATERAL # noqa 503
                f"{format_number_display(position['ratio'] * 100, 0, 2)}%",  # COLLAT % # noqa 503
            )

        print_table(table)


@app.command()
def rebalance(
    network: IcxNetwork = typer.Option(
        Config.get_default_network(),
        "--network",
        "-n",
        callback=Callbacks.enforce_mainnet,
        case_sensitive=False,
    )
):
    balanced_loans = BalancedLoans(network)
    rebalance_status = balanced_loans.query_rebalance_status()
    if hex_to_int(rebalance_status[0]) == 1:
        print(
            f"Forward Rebalancing: Sell {hex_to_int(rebalance_status[1]) / 10 ** 18} tokens"
        )  # noqa 503
    elif hex_to_int(rebalance_status[2]) == 1:
        print(
            f"Reverse Rebalancing: Sell {hex_to_int(rebalance_status[1]) / 10 ** 18} tokens"
        )  # noqa 503
    else:
        print("No rebalancing is necessary at this time.")


@app.command()
def claim(
    transaction_hash: str = typer.Argument(...),
    network: IcxNetwork = typer.Option(
        Config.get_default_network(),
        "--network",
        "-n",
        callback=Callbacks.enforce_mainnet,
        case_sensitive=False,
    ),
    format: str = typer.Option(
        None, "--format", "-f", callback=Callbacks.validate_output_format
    ),
):
    balanced_dividends = BalancedDividends(network)
    claim = balanced_dividends.calculate_claim_in_usd(transaction_hash)
    print(claim)
