import typer
from icon_cli.models.Config import Config
from icon_cli.utils import print_json

app = typer.Typer()

config = Config()


@app.command()
def debug():
    typer.echo(__name__)


@app.command()
def inspect(
    keystore_name=typer.Argument(config.get_default_keystore()),
    all: bool = typer.Option(False, "--all", "-a"),
    format: str = typer.Option(None, "--format", "-f"),
):
    """
    Returns information about imported keystores.
    """

    if all is True:
        imported_keystores = config.get_imported_keystores()
        if format == "json":
            print_json(imported_keystores)
        else:
            for keystore in imported_keystores:
                print(
                    f"Keystore Name: {keystore['keystore_name']}\n"
                    f"Keystore Address: {keystore['keystore_address']}\n"
                    f"Keystore Filename: {keystore['keystore_filename']}"
                )
    else:
        keystore_metadata = config.get_keystore_metadata(keystore_name)
        if format == "json":
            print_json(keystore_metadata)
        else:
            print(
                f"Keystore Name: {keystore_metadata['keystore_name']}\n"
                f"Keystore Address: {keystore_metadata['keystore_address']}\n"
                f"Keystore Filename: {keystore_metadata['keystore_filename']}"
            )
