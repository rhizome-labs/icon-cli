import io
import json
import os
import shutil
from pathlib import Path, PosixPath

import typer
import yaml
from iconsdk.wallet.wallet import KeyWallet
from rich import print

from icon_cli.models import AppConfig, IcxNetwork
from icon_cli.utils import Utils


class Config:

    CONFIG_DIR = f"{Path.home()}/.icon-cli"
    CONFIG_FILE = f"{CONFIG_DIR}/config.yml"
    DATA_DIR = f"{CONFIG_DIR}/data"
    KEYSTORE_DIR = f"{CONFIG_DIR}/keystore"
    HISTORY_DIR = f"{CONFIG_DIR}/history"

    REQUIRED_DIRS = [CONFIG_DIR, DATA_DIR, HISTORY_DIR, KEYSTORE_DIR]

    DEFAULT_CONFIG = AppConfig()

    DEFAULT_NETWORKS = {
        "mainnet": IcxNetwork(
            api_endpoint="https://ctz.solidwallet.io",
            nid=1,
            tracker_endpoint="https://tracker.icon.community",
        ),
        "lisbon": IcxNetwork(
            api_endpoint="https://lisbon.net.solidwallet.io",
            nid=2,
            tracker_endpoint="https://lisbon.tracker.solidwallet.io",
        ),
        "berlin": IcxNetwork(
            api_endpoint="https://berlin.net.solidwallet.io",
            nid=7,
            tracker_endpoint="https://berlin.tracker.solidwallet.io",
        ),
        "sejong": IcxNetwork(
            api_endpoint="https://sejong.net.solidwallet.io",
            nid=83,
            tracker_endpoint="https://sejong.tracker.solidwallet.io",
        ),
    }

    def __init__(self) -> None:
        pass

    @classmethod
    def initialize(cls, validate_config_file: bool = True) -> None:
        """
        An initialization function that ensures required directories and config file exists.
        """
        # Loop through required directories, and create the directory if it doesn't exist.
        for directory in cls.REQUIRED_DIRS:
            if not Path(directory).is_dir():
                print(f"{directory} does not exist. Creating directory now...")
                cls._create_directory(directory)

        # Create a config file with the contents of DEFAULT_CONFIG if it does not exist.
        if not os.path.exists(cls.CONFIG_FILE):
            print(f"Creating config file at {cls.CONFIG_FILE} now...")
            with open(cls.CONFIG_FILE, "w+", encoding="utf-8") as CONFIG_FILE:
                yaml.dump(cls.DEFAULT_CONFIG, CONFIG_FILE, sort_keys=True)

        return

    @classmethod
    def read(cls) -> dict:
        with open(cls.CONFIG_FILE, "r") as f:
            config = yaml.safe_load(f)
        return config

    @staticmethod
    def _copy_file(source, destination) -> None:
        shutil.copyfile(source, destination)

    @staticmethod
    def _create_directory(path: PosixPath) -> None:
        os.mkdir(path)

    @staticmethod
    def _delete_file(path: PosixPath) -> None:
        os.remove(path)
