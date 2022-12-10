import os
import shutil
from datetime import datetime
from pathlib import Path

import typer
from rich import print

from icon_cli.config import Config
from icon_cli.utils import Utils
from icon_cli.validators import Validators

app = typer.Typer()


@app.command()
def add(
    keystore_path: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        readable=True,
        resolve_path=True,
        callback=Validators.validate_keystore_file,
        help="File path to an ICX keystore file.",
    )
) -> None:
    """
    Import an existing ICX keystore file into icon-cli.
    """
    # Prompt user for a keystore name.
    keystore_name = typer.prompt("Please specify a nickname for this keystore")  # fmt: skip
    keystore_name = keystore_name.casefold()
    keystore_filename = f"{keystore_name}.json"

    # Get filenames of imported keystores.
    imported_keystores = Config.get_imported_keystore_filenames()

    # Check if there is an imported keystore with a conflicting filename.
    if keystore_filename in imported_keystores:

        # Ask user if they want to remove the existing keystore with the same filename.
        remove_existing_keystore_prompt = typer.confirm(
            (
                f"There is an existing keystore with the nickname {keystore_name}.\n"
                f"Would you like to replace the existing keystore with this one?"
            )
        )
        if remove_existing_keystore_prompt is True:
            try:
                removed_keystore_file_path = f"{Config.TRASH_DIR}/{int(datetime.utcnow().timestamp())}_{keystore_filename}"
                os.rename(f"{Config.KEYSTORE_DIR}/{keystore_filename}", removed_keystore_file_path)  # fmt: skip
                print(
                    (
                        f"The existing keystore has been moved to {removed_keystore_file_path}.\n"
                        f"To empty the trash, run the `icon config purge` command."
                    ),
                )
            except:
                Utils.exit("There was an issue with removing the keystore file.", "error")  # fmt: skip
        else:
            Utils.exit("Please re-run this command and specify another name.", "ok")  # fmt: skip

    # Copy keystore file to .icon-cli/keystore
    try:
        shutil.copyfile(keystore_path, f"{Config.KEYSTORE_DIR}/{keystore_filename}")
    except:
        Utils.exit("There was an issue with copying the keystore file to ~/.icon-cli/keystore.", "error")  # fmt: skip

    # Load current icon-cli config.
    config = Config.read_config()

    # Ask user if they want to set current keystore to default keystore.
    default_keystore_prompt = typer.confirm(
        f"Would you like to set {keystore_name} as the default keystore for icon-cli?"
    )
    # If user answers YES, write default keystore to the config file.
    if default_keystore_prompt is True:
        config.default_keystore = keystore_name
        Config.write_config(config)

    Utils.exit(f"{keystore_name} has been imported!.", "success")  # fmt: skip


@app.command()
def list():
    """
    List keystores that have been imported into icon-cli.
    """
    imported_keystores = Config.get_imported_keystore_filenames()
    Utils.print_json(
        {
            os.path.splitext(keystore)[0]: Config.get_keystore_public_key(keystore)
            for keystore in imported_keystores
        }
    )


@app.command()
def set(keystore_name: str):
    """
    Set the default keystore for icon-cli.
    """
    imported_keystore_nicknames = Config.get_imported_keystore_nicknames()
    if keystore_name not in keystore_name:
        Utils.exit(f"{keystore_name} is not an imported keystore.")
