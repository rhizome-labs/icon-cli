import os
from pathlib import Path

import yaml

from icon_cli.models import AppConfig, IcxNetwork

EXA = 10**18

CONFIG_DIR = f"{Path.home()}/.icon-cli"
CONFIG_FILE = f"{CONFIG_DIR}/config.yml"
DATA_DIR = f"{CONFIG_DIR}/data"
KEYSTORE_DIR = f"{CONFIG_DIR}/keystore"
HISTORY_DIR = f"{CONFIG_DIR}/history"
TRASH_DIR = f"{CONFIG_DIR}/.trash"
REQUIRED_DIRS = [CONFIG_DIR, DATA_DIR, HISTORY_DIR, KEYSTORE_DIR, TRASH_DIR]

DEFAULT_CONFIG = AppConfig()

DEFAULT_NETWORKS = {
    "mainnet": IcxNetwork(
        name="mainnet",
        api_endpoint="https://api.icon.community",
        nid=1,
        tracker_endpoint="https://tracker.icon.community",
    ),
    "lisbon": IcxNetwork(
        name="lisbon",
        api_endpoint="https://lisbon.net.solidwallet.io",
        nid=2,
        tracker_endpoint="https://lisbon.tracker.solidwallet.io",
    ),
    "berlin": IcxNetwork(
        name="berlin",
        api_endpoint="https://berlin.net.solidwallet.io",
        nid=7,
        tracker_endpoint="https://berlin.tracker.solidwallet.io",
    ),
    "sejong": IcxNetwork(
        name="sejong",
        api_endpoint="https://sejong.net.solidwallet.io",
        nid=83,
        tracker_endpoint="https://sejong.tracker.solidwallet.io",
    ),
}

ICX_KEYSTORE_JSON_SCHEMA = {
    "type": "object",
    "properties": {
        "version": {"type": "integer"},
        "id": {"type": "string"},
        "address": {"type": "string"},
        "crypto": {
            "type": "object",
            "properties": {
                "ciphertext": {"type": "string"},
                "cipherparams": {
                    "type": "object",
                    "properties": {"iv": {"type": "string"}},
                },
                "cipher": {"type": "string"},
                "kdf": {"type": "string"},
                "kdfparams": {
                    "type": "object",
                    "properties": {
                        "dklen": {"type": "integer"},
                        "salt": {"type": "string"},
                        "n": {"type": "integer"},
                        "r": {"type": "integer"},
                        "p": {"type": "integer"},
                    },
                },
                "mac": {"type": "string"},
            },
        },
        "coinType": {"type": "string"},
    },
}


def initialize() -> None:
    """
    An initialization function that ensures required directories and config file exists.
    """
    # Loop through required directories, and create the directory if it doesn't exist.
    for directory in REQUIRED_DIRS:
        if not Path(directory).is_dir():
            print(f"{directory} does not exist. Creating directory now...")
            os.mkdir(directory)

    # Create a config file with the contents of DEFAULT_CONFIG if it does not exist.
    if not os.path.exists(CONFIG_FILE):
        print(f"Creating config file at {CONFIG_FILE} now...")
        with open(CONFIG_FILE, "w+", encoding="utf-8") as f:
            yaml.safe_dump(DEFAULT_CONFIG.dict(), f)

    with open(CONFIG_FILE, "r") as f:
        config = yaml.safe_load(f)

    return AppConfig(**config)


CONFIG = initialize()
