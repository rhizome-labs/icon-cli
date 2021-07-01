import typer
from icon_cli.models.Callbacks import Callbacks
from icon_cli.models.Config import Config
from icon_cli.models.Prep import Prep
from icon_cli.utils import print_json

app = typer.Typer()

callbacks = Callbacks()
config = Config()


@app.command()
def debug():
    typer.echo(__name__)


@app.command()
def preps(
    network: str = typer.Option(Config.get_default_network(), "--network", "-n", callback=Callbacks.enforce_mainnet),
    range_start: int = typer.Option(1, "--start", "-s"),
    range_end: int = typer.Option(Prep.query_prep_count(), "--end", "-e"),
    format: str = typer.Option(None, "--format", "-f", callback=Callbacks.validate_output_format),
):
    prep = Prep(network)
    preps = prep.query_preps(range_start, range_end)

    if format == "json":
        print_json(preps)
    else:
        print(preps)
