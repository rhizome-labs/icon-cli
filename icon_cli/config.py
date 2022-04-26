import os
import shutil
from pathlib import Path, PosixPath

import yaml


class Config:

    config_dir = f"{Path.home()}/.icon-cli"
    config_file = f"{config_dir}/config.yml"
    data_dir = f"{config_dir}/data"
    keystore_dir = f"{config_dir}/keystore"
    history_dir = f"{config_dir}/history"

    default_config = {
        "custom_endpoints": [],
        "default_keystore": None,
        "default_network": "mainnet",
        "keystores": [],
        "query_only": False,
        "saved_addresses": [],
    }

    default_networks = {
        "mainnet": {
            "api_endpoint": "https://ctz.solidwallet.io",
            "nid": 1,
            "tracker_endpoint": "https://tracker.icon.community",
        },
        "lisbon": {
            "api_endpoint": "https://lisbon.net.solidwallet.io",
            "nid": 2,
            "tracker_endpoint": "https://lisbon.tracker.solidwallet.io",
        },
        "berlin": {
            "api_endpoint": "https://berlin.net.solidwallet.io",
            "nid": 7,
            "tracker_endpoint": "https://berlin.tracker.solidwallet.io",
        },
        "sejong": {
            "api_endpoint": "https://sejong.net.solidwallet.io",
            "nid": 83,
            "tracker_endpoint": "https://sejong.tracker.solidwallet.io",
        },
    }

    def __init__(self) -> None:
        pass

    @classmethod
    def initialize_config(cls) -> None:

        required_dirs = [
            cls.config_dir,
            cls.data_dir,
            cls.history_dir,
            cls.keystore_dir,
        ]

        for dir in required_dirs:
            if not Path(dir).is_dir():
                print(f"{dir} does not exist. Creating directory now...")
                cls._create_directory(dir)

        if not os.path.exists(cls.config_file):
            print(f"Creating config file at {cls.config_file} now...")
            with open(cls.config_file, "w+", encoding="utf-8") as config_file:
                yaml.dump(cls.default_config, config_file, sort_keys=True)

    ######################
    # NETWORK FUNCTIONS #
    ######################

    @classmethod
    def get_default_network(cls) -> str:
        config = cls._read_config()
        default_network = config["default_network"]
        return default_network

    @classmethod
    def get_default_networks(cls) -> dict:
        return cls.default_networks

    ##############################
    # EXTERNAL UTILITY FUNCTIONS #
    ##############################

    @classmethod
    def inspect_config(cls) -> dict:
        return cls._read_config()

    @classmethod
    def _read_config(cls) -> dict:
        with open(cls.config_file, "r") as config_file:
            config = yaml.safe_load(config_file)
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
