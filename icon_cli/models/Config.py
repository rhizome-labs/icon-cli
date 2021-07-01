import hashlib
import io
import json
import os
import requests
import shutil
import typer
import yaml
from pathlib import Path, PosixPath


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
        "mainnet": ["https://ctz.solidwallet.io", 1],
        "euljiro": ["https://test-ctz.solidwallet.io", 2],
        "yeouido": ["https://bicon.net.solidwallet.io", 3],
        "local": ["http://localhost:9000", 3],
    }

    @classmethod
    def initialize_config(cls) -> None:

        required_directories = [
            cls.config_dir,
            cls.data_dir,
            cls.history_dir,
            cls.keystore_dir,
        ]

        for directory in required_directories:
            if not Path(directory).is_dir():
                print(f"{directory} does not exist. Creating directory now...")
                cls._create_directory(directory)

        if not os.path.exists(cls.config_file):
            print(f"Creating config file at {cls.config_file} now...")
            with open(cls.config_file, "w+", encoding="utf-8") as config_file:
                yaml.dump(cls.default_config, config_file, sort_keys=True)
                print(f"Config file has been successfully created at {cls.config_file}.")

    @classmethod
    def inspect_config(cls) -> dict:
        return cls._read_config()

    ######################
    # KEYSTORE FUNCTIONS #
    ######################

    @classmethod
    def get_default_keystore(cls) -> str:
        config = cls._read_config()
        default_keystore = config["default_keystore"]
        return default_keystore

    @classmethod
    def get_imported_keystores(cls) -> list:
        config = cls._read_config()
        return config["keystores"]

    @classmethod
    def get_keystore_metadata(cls, keystore_name) -> dict:
        config = cls._read_config()
        for imported_keystore in config["keystores"]:
            if keystore_name == imported_keystore["keystore_name"]:
                return imported_keystore

    #####################
    # NETWORK FUNCTIONS #
    #####################

    @classmethod
    def get_default_network(cls) -> str:
        config = cls._read_config()
        default_network = config["default_network"]
        return default_network

    @classmethod
    def get_default_networks(cls) -> dict:
        return cls.default_networks

    @classmethod
    def set_default_network(cls, network: str) -> None:
        if network in cls.default_networks.keys():
            try:
                print(f"Setting default network to {network}.")
                cls._write_config("default_network", network)
                print(f"Success! Default network has been set to {network}.")
            except Exception as e:
                print(e)
                raise typer.Exit()
        else:
            print(f"{network} is not a supported network.")
            raise typer.Exit()

    ##############################
    # EXTERNAL UTILITY FUNCTIONS #
    ##############################

    @classmethod
    def list_imported_keystore_names(cls):
        config = cls._read_config()
        imported_keystores = config["keystores"]
        if len(imported_keystores) > 0:
            keystore_names = [keystore["keystore_name"] for keystore in imported_keystores]
            return keystore_names
        else:
            print("There are no imported keystores.")
            raise typer.Exit()

    @staticmethod
    def ping():
        requests.head("https://icon-cli-analytics.rhizome.workers.dev", timeout=0.5)

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
            print("Sorry, only string values are supported.")
            raise typer.Exit()
        if key in cls._list_config_keys():
            with open(cls.config_file, "r+", encoding="utf-8") as config_file:  # noqa 503
                config = yaml.full_load(config_file)
                config[key] = value
                config_file.seek(0)
                yaml.dump(config, config_file, sort_keys=True)
                config_file.truncate()
        else:
            print(f"Sorry, {key} is not a valid configuration key.")
            raise typer.Exit()

    @classmethod
    def _read_keystore(cls, keystore_path: str) -> tuple:
        with io.open(keystore_path, "r", encoding="utf-8-sig") as keystore_file:
            keystore_json = json.load(keystore_file)
            keystore_address = keystore_json["address"]
        keystore_hash = hashlib.md5(open("/Users/brianli/Desktop/testnet-keystore", "rb").read()).hexdigest()
        return keystore_json, keystore_address, keystore_hash
