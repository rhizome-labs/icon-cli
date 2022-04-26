import os
import shutil
from pathlib import Path, PosixPath

import yaml
from rich import print

from icon_cli.utils import die


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
        "saved_addresses": {},
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

    @classmethod
    def inspect_config(cls) -> dict:
        return cls._read_config()

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

    ##########################
    # ADDRESS BOOK FUNCTIONS #
    ##########################

    @classmethod
    def add_address_to_address_book(cls, address: str, name: str):
        with open(cls.config_file, "r+", encoding="utf-8") as config_file:
            config = yaml.safe_load(config_file)
            config["saved_addresses"][name] = address
            config_file.seek(0)
            yaml.dump(config, config_file, sort_keys=True)
            config_file.truncate()

    @classmethod
    def delete_address_from_address_book(cls, name: str):
        with open(cls.config_file, "r+", encoding="utf-8") as config_file:
            config = yaml.safe_load(config_file)
            config["saved_addresses"].pop(name)
            config_file.seek(0)
            yaml.dump(config, config_file, sort_keys=True)
            config_file.truncate()

    ##############################
    # INTERNAL UTILITY FUNCTIONS #
    ##############################

    @staticmethod
    def _copy_file(source, destination) -> None:
        shutil.copyfile(source, destination)

    @staticmethod
    def _create_directory(path: PosixPath) -> None:
        os.mkdir(path)

    @staticmethod
    def _delete_file(path: PosixPath) -> None:
        os.remove(path)

    @classmethod
    def _list_config_keys(cls) -> str:
        keys = list(cls.default_config.keys())
        return ", and ".join([", ".join(keys[:-1]), keys[-1]])

    @classmethod
    def _read_config(cls) -> dict:
        with open(cls.config_file, "r") as config_file:
            config = yaml.full_load(config_file)
        return config

    @classmethod
    def _write_config(cls, key: str, value: str):
        if not isinstance(value, str):
            die("Only string values are supported.", "error")
        if key in cls._list_config_keys():
            with open(
                cls.config_file, "r+", encoding="utf-8"
            ) as config_file:  # noqa 503
                config = yaml.safe_load(config_file)
                config[key] = value
                config_file.seek(0)
                yaml.dump(config, config_file, sort_keys=True)
                config_file.truncate()
        else:
            die(f"{key} is not a valid configuration key.", "error")
