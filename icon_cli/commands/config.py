import os
import shutil
from datetime import datetime
from pathlib import Path

import typer
from rich import print

from icon_cli.config import Config
from icon_cli.utils import Utils

app = typer.Typer()


@app.command()
def import_keystore(
    keystore_path: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        readable=True,
        resolve_path=True,
        callback=Utils.validate_keystore_file,
    )
) -> None:

    # Prompt user for a keystore name.
    keystore_name = typer.prompt("Please specify a nickname for this keystore")  # fmt: skip
    keystore_name = keystore_name.casefold()
    keystore_filename = f"{keystore_name}.json"

    # Get filenames of imported keystores.
    imported_keystores = Config.get_imported_keystores()

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
def mode() -> None:
    """
    Change the icon-cli mode between read-only and read/write modes.
    """
    # Read config.
    config = Config.read_config()

    # Prompt user to change to "rw" mode if current mode is "r".
    if config.mode == "r":
        mode_prompt = typer.confirm(
            f"icon-cli is currently in read-only mode. Do you want to switch to read/write mode?"
        )
        if mode_prompt is True:
            config.mode = "rw"
            Config.write_config(config)
            print(f"SUCCESS: icon-cli has been set to read/write mode.")
    # Prompt user to change to "r" mode if current mode is "rw".
    else:
        mode_prompt = typer.confirm(
            f"icon-cli is currently in read/write mode. Do you want to switch to read-only mode?"
        )
        if mode_prompt is True:
            config.mode = "r"
            Config.write_config(config)
            print(f"SUCCESS: icon-cli has been set to read-only mode.")


@app.command()
def network(network: str = typer.Argument(...)) -> None:
    """
    Change the default network in config.yml

    Args:
        network: The name of the network to set. Supported values are "mainnet", "lisbon", "berlin", and "sejong".
    """
    # Die if network not in DEFAULT_NETWORKS. This will be changed later when custom networks are supported.
    if network not in Config.DEFAULT_NETWORKS.keys():
        Utils.exit(f"{network} is not a supported network.", "error")

    # Read config.
    config = Config.read_config()
    # Set default network to provided network.
    config.default_network = network
    # Write config to disk.
    Config.write_config(config)
    print(f"SUCCESS: Default network has been set to {network}.")


@app.command()
def purge():
    purge_confirmation_prompt = typer.confirm(
        f"Are you sure you want to permanently delete the contents of {Utils.abs_path('~/.icon-cli/.trash')}?"
    )
    if purge_confirmation_prompt is True:
        # Delete .trash directory.
        shutil.rmtree(Config.TRASH_DIR)
        # Create .trash directory.
        os.mkdir(Config.TRASH_DIR)
        Utils.exit(
            f"{Utils.abs_path('~/.icon-cli/.trash')} has been purged.", "success"
        )


@app.command()
def view() -> None:
    """
    Prints a dictionary representation of config.yml.
    """
    # Read config.
    config = Config.read_config()
    print(config.dict())
