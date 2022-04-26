import typer
from icon_cli.config import Config
from icon_cli.commands.subcommands.config import keystore
from icon_cli.utils import die, print_json, print_object

app = typer.Typer()

app.add_typer(keystore.app, name="keystore")


@app.command()
def debug():
    print_object(__name__)


@app.command()
def init():
    confirmation = typer.confirm(
        "This will delete your existing config.yml file, and generate a new config.yml file. Please confirm."
    )
    if confirmation:
        Config.delete_config()
        Config.initialize_config()
    else:
        die()


@app.command()
def inspect():
    config = Config.inspect_config()
    print_json(config)
