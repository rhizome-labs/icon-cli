import os
import shutil
from datetime import datetime
from pathlib import Path

import typer
from rich import print

from icon_cli.commands.config import keystore
from icon_cli.config import Config
from icon_cli.utils import Utils

app = typer.Typer()

app.add_typer(keystore.app, name="keystore")


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
