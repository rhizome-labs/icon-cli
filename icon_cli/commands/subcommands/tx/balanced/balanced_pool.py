import typer
from icon_cli.utils import format_number_display, log, print_object, print_tx_hash, to_loop
from rich import print

app = typer.Typer()


@app.command()
def debug():
    print_object(__name__)
