import io
import json
import os
import shutil
from pathlib import Path

import yaml

from icon_cli.models import AppConfig, IcxNetwork


class Config:

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
            with open(cls.CONFIG_FILE, "w+", encoding="utf-8") as f:
                yaml.safe_dump(cls.DEFAULT_CONFIG.dict(), f)

        return

    @classmethod
    def get_default_keystore(cls) -> str:
        config = cls._read_config()
        default_keystore = config.default_keystore
        return default_keystore

    @classmethod
    def get_default_network(cls) -> str:
        config = cls._read_config()
        default_network = config.default_network
        return default_network

    @classmethod
    def read_config(cls) -> AppConfig:
        config = cls._read_config()
        return config

    @classmethod
    def write_config(cls, config: AppConfig) -> None:
        """
        Writes an AppConfig object to config.yml file on disk.

        Args:
            config: An AppConfig object containing an icon-cli configuration.
        """
        with open(cls.CONFIG_FILE, "w+") as f:
            yaml.safe_dump(config.dict(), f)
        return

    ####################
    # KEYSTORE METHODS #
    ####################

    @classmethod
    def get_imported_keystore_filenames(cls) -> list:
        files_in_keystore_dir = os.listdir(cls.KEYSTORE_DIR)
        if len(files_in_keystore_dir) == 0:
            return []
        else:
            return files_in_keystore_dir

    @classmethod
    def get_imported_keystore_nicknames(cls) -> list:
        files_in_keystore_dir = os.listdir(cls.KEYSTORE_DIR)
        if len(files_in_keystore_dir) == 0:
            return []
        else:
            return [
                os.path.splitext(keystore_filename)[0]
                for keystore_filename in files_in_keystore_dir
            ]

    @classmethod
    def get_keystore_public_key(cls, keystore_filename: Path) -> str:
        keystore_data = cls.read_keystore(f"{cls.KEYSTORE_DIR}/{keystore_filename}")
        public_key = keystore_data["address"]
        return public_key

    @classmethod
    def read_keystore(cls, keystore_path: Path) -> tuple:
        # Open keystore file.
        with io.open(keystore_path, "r", encoding="utf-8-sig") as keystore_file:
            keystore_data = json.load(keystore_file)
        return keystore_data

    ####################
    # INTERNAL METHODS #
    ####################

    @classmethod
    def _read_config(cls) -> AppConfig:
        with open(cls.CONFIG_FILE, "r") as f:
            data = yaml.safe_load(f)
            config = AppConfig(**data)
        return config

    @staticmethod
    def _copy_file(source, destination) -> None:
        shutil.copyfile(source, destination)

    @staticmethod
    def _create_directory(path: Path) -> None:
        os.mkdir(path)

    @staticmethod
    def _delete_file(path: Path) -> None:
        os.remove(path)
