import typer
from rich.pretty import pprint

from icon_cli.config import Config
from icon_cli.utils import Utils

app = typer.Typer()


@app.command()
def view() -> None:
    """
    Prints a dictionary representation of config.yml.
    """
    config = Config.read_config()
    pprint(config.dict(), expand_all=True)


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
            pprint(f"SUCCESS: icon-cli has been set to read/write mode.")
    # Prompt user to change to "r" mode if current mode is "rw".
    else:
        mode_prompt = typer.confirm(
            f"icon-cli is currently in read/write mode. Do you want to switch to read-only mode?"
        )
        if mode_prompt is True:
            config.mode = "r"
            Config.write_config(config)
            pprint(f"SUCCESS: icon-cli has been set to read-only mode.")


@app.command()
def set_network(network: str = typer.Argument(...)) -> None:
    """
    Change the default network in config.yml

    Args:
        network: The name of the network to set. Supported values are "mainnet", "lisbon", "berlin", and "sejong".
    """
    # Die if network not in DEFAULT_NETWORKS. This will be changed later when custom networks are supported.
    if network not in Config.DEFAULT_NETWORKS.keys():
        Utils.die(f"{network} is not a supported network.", "error")

    # Read config.
    config = Config.read_config()
    # Set default network to provided network.
    config.default_network = network
    # Write config to disk.
    Config.write_config(config)
    pprint(f"SUCCESS: Default network has been set to {network}.")
