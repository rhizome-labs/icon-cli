import typer
from icon_cli.models.Callbacks import Callbacks
from icon_cli.models.Config import Config
from icon_cli.models.Gov import Gov
from icon_cli.models.Prep import Prep
from icon_cli.utils import format_number_display, print_json, print_object, print_table
from rich import box
from rich import print
from rich.table import Table

app = typer.Typer()

callbacks = Callbacks()
config = Config()


@app.command()
def debug():
    print_object(__name__)


@app.command()
def preps(
    network: str = typer.Option(Config.get_default_network(), "--network", "-n", callback=Callbacks.enforce_mainnet),
    range_start: int = typer.Option(1, "--start", "-s"),
    range_end: int = typer.Option(500, "--end", "-e"),
    format: str = typer.Option(None, "--format", "-f", callback=Callbacks.validate_output_format),
):
    if range_start < 1:
        print("Range start must be greater than 1.")
        raise typer.Exit()
    if range_end < range_start:
        print("Range end must be greater than range start.")
        raise typer.Exit()

    prep = Prep(network)
    preps = prep.query_preps(range_start, range_end)

    if format == "json":
        print_json(preps)
    else:
        print(preps)


@app.command()
def delegation(
    address: str = typer.Option(None, "--address", "-a", callback=Callbacks.validate_icx_address),
    keystore: str = typer.Option(
        Config.get_default_keystore(), "--keystore", "-k", callback=Callbacks.validate_keystore_name
    ),
    network: str = typer.Option(Config.get_default_network(), "--network", "-n", callback=Callbacks.enforce_mainnet),
    format: str = typer.Option(None, "--format", "-f", callback=Callbacks.validate_output_format),
):
    gov = Gov(network)

    if address is None:
        address = Config.get_keystore_metadata(keystore)["keystore_address"]

    delegations = gov.query_delegation(address)

    if format == "json":
        print_json(delegations)
    else:
        table = Table(
            box=box.DOUBLE,
            show_lines=True,
            show_header=False,
            title="Delegation Details",
            title_justify="left",
            title_style="bold",
        )

        table.add_column("Key", justify="left", style="bold")
        table.add_column("Value", justify="left")

        table.add_row("ADDRESS", address)
        table.add_row("TOTAL DELEGATION", f"{format_number_display(delegations['totalDelegated'])} ICX")
        for delegation in delegations["delegations"]:
            table.add_row(
                Prep.convert_address_to_name(delegation["address"]), f"{format_number_display(delegation['value'])} ICX"
            )

        print_table(table)
