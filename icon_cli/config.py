import io
import json
import os
import shutil
from pathlib import Path, PosixPath

import typer
import yaml
from iconsdk.wallet.wallet import KeyWallet
from rich import print

from icon_cli.utils import die, log


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

    ####################
    # WALLET FUNCTIONS #
    ####################

    @classmethod
    def get_keystore_metadata(cls, keystore: str) -> dict:
        config = cls._read_config()
        for imported_keystore in config["keystores"]:
            if keystore == imported_keystore["keystore_name"]:
                return imported_keystore

    @classmethod
    def get_default_keystore(cls) -> str:
        config = cls._read_config()
        return config["default_keystore"]

    @classmethod
    def create_keystore(cls) -> None:
        keystore = KeyWallet.create()
        print(keystore)

    @classmethod
    def import_keystore(cls, keystore_path: PosixPath) -> None:

        # Get keystore metadata, and calculate hash.
        keystore = cls._read_keystore(keystore_path)
        keystore_address = keystore["address"]

        # Read icon-cli configuration, and get keystore config.
        config = cls._read_config()
        default_keystore_config = config["default_keystore"]
        keystore_config = config["keystores"]

        if len(keystore_config) > 0:
            for imported_keystore in keystore_config:
                if keystore_address == imported_keystore["keystore_address"]:
                    die(
                        f"An imported keystore ({imported_keystore['keystore_name']}) with the address {keystore_address} already exists.",
                        "error",
                    )

        # Prompt user to specify a nickname for the keystore.
        keystore_name = typer.prompt("Please specify a nickname for this keystore")

        if len(keystore_config) > 0:
            for imported_keystore in keystore_config:
                if keystore_name == imported_keystore["keystore_name"]:
                    die(
                        f"An imported keystore named {keystore_name} already exists.",
                        "error",
                    )

        # If there are no existing keystores, or if default keystore is not set, prompt user to choose whether to set keystore as default. # noqa 503
        if default_keystore_config is None:
            default_keystore_prompt = typer.confirm(
                f"There is no existing keystore. Would you like to make {keystore_name} the default keystore?"
            )
            if default_keystore_prompt:
                with open(cls.config_file, "r+", encoding="utf-8") as config_file:
                    cls._write_config("default_keystore", keystore_name)

        # Copy keystore to ~/.icon-cli/keystore
        cls._copy_file(
            f"{keystore_path}", f"{cls.config_dir}/keystore/{keystore_address}.icx"
        )

        # Create JSON payload to write to config.
        keystore_data = {
            "keystore_name": keystore_name,
            "keystore_address": keystore_address,
            "keystore_filename": f"{keystore_address}.icx",
        }

        # Write keystore name and address to config.json.
        with open(cls.config_file, "r+", encoding="utf-8") as config_file:
            config = yaml.full_load(config_file)
            config["keystores"].append(keystore_data)
            config_file.seek(0)
            yaml.dump(config, config_file, sort_keys=True)
            config_file.truncate()

        print("Keystore has been imported successfully.")

    @classmethod
    def _read_keystore(cls, keystore_path: PosixPath) -> tuple:
        with io.open(keystore_path, "r", encoding="utf-8-sig") as keystore_file:
            keystore = json.load(keystore_file)
            return keystore

    ######################
    # NETWORK FUNCTIONS #
    ######################

    @classmethod
    def get_default_network(cls) -> str:
        try:
            config = cls._read_config()
            default_network = config["default_network"]
        except KeyError:
            default_network = "mainnet"
        return default_network

    @classmethod
    def get_default_networks(cls) -> dict:
        return cls.default_networks

    @classmethod
    def set_default_network(cls, network) -> None:
        with open(cls.config_file, "r+", encoding="utf-8") as config_file:
            config = yaml.safe_load(config_file)
            config["default_network"] = network
            config_file.seek(0)
            yaml.dump(config, config_file, sort_keys=True)
            config_file.truncate()

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
