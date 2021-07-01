import typer
from icon_cli.models.Callbacks import Callbacks
from icon_cli.models.Config import Config
from icon_cli.utils import print_json, print_object
from pathlib import Path

app = typer.Typer()


@app.command()
def debug():
    print_object(__name__)


@app.command()
def add(
    keystore_path: Path = typer.Argument(
        ...,
        callback=Callbacks.validate_keystore_integrity,
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        writable=False,
        resolve_path=True,
    )
):
    """
    Add a keystore to ~/.icon-cli/keystore.
    """
    Config.import_keystore(keystore_path)


@app.command()
def inspect(
    keystore_name=typer.Argument(Config.get_default_keystore(), callback=Callbacks.validate_keystore_name),
    all: bool = typer.Option(False, "--all", "-a"),
    format: str = typer.Option(None, "--format", "-f", callback=Callbacks.validate_output_format),
):
    """
    Returns information about imported keystores.
    """

    if all is True:
        imported_keystores = Config.get_imported_keystores()
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
        keystore_metadata = Config.get_keystore_metadata(keystore_name)
        if format == "json":
            print_json(keystore_metadata)
        else:
            print(
                f"Keystore Name: {keystore_metadata['keystore_name']}\n"
                f"Keystore Address: {keystore_metadata['keystore_address']}\n"
                f"Keystore Filename: {keystore_metadata['keystore_filename']}"
            )
