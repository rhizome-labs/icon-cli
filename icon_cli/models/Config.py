import hashlib
import io
import json
import os
import shutil
import typer
import yaml
from pathlib import Path, PosixPath


class Config:

    config_dir_path = f"{Path.home()}/.icon-cli"
    config_file_path = f"{config_dir_path}/config.yml"
    data_dir_path = f"{config_dir_path}/data"
    keystore_dir_path = f"{config_dir_path}/keystore"
    history_dir_path = f"{config_dir_path}/history"

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

    icx_governance_contract = "cx0000000000000000000000000000000000000001"
    iiss_contract = "cx0000000000000000000000000000000000000000"

    irc2_token_tickers = {
        "BALN": "cxf61cd5a45dc9f91c15aa65831a30a90d59a09619",
        "TAP": "cxc0b5b52c9f8b4251a47e91dda3bd61e5512cd782",
    }

    def __init__(self) -> None:
        pass

    ############################
    # INITIALIZATION FUNCTIONS #
    ############################

    @classmethod
    def initialize_config(cls) -> None:

        # Check if config.json file doesn't exist.
        if not os.path.exists(cls.config_file_path):

            # List required directories.
            required_directories = [
                cls.config_dir_path,
                cls.data_dir_path,
                cls.history_dir_path,
                cls.keystore_dir_path,
            ]

            # Loop through required directories and create directory if it doesn't exist.
            for directory in required_directories:
                if not Path(directory).is_dir():
                    print(f"{directory} does not exist. Creating directory now...")
                    cls._create_directory(directory)

            # Create config.json file if it doesn't exist.
            print(f"Creating config file at {cls.config_file_path} now...")
            with open(cls.config_file_path, "w", encoding="utf-8") as config_file_path:
                yaml.dump(cls.default_config, config_file_path, sort_keys=True)
                print(f"config file has been successfully created at {cls.config_file_path}.")

    ##############################
    # KEYSTORE-RELATED FUNCTIONS #
    ##############################

    @classmethod
    def import_keystore(cls, keystore_path: PosixPath) -> None:
        # Get keystore address.
        _, keystore_address, keystore_hash = cls._read_keystore(keystore_path)  # noqa 503

        # Read icon-cli configuration, and get keystore config.
        config = cls._read_config()
        default_keystoreconfig = config["default_keystore"]
        keystore_config = config["keystores"]

        # Check if address is already used in imported keystores.
        if len(keystore_config) > 0:
            for imported_keystore in keystore_config:
                if keystore_address == imported_keystore["keystore_address"]:
                    print(
                        f"An imported keystore ({imported_keystore['keystore_name']}) with the address {keystore_address} already exists."  # noqa 503
                    )
                    print("Exiting now...")
                    raise typer.Exit()

        # Prompt user to specify a nickname for the keystore.
        keystore_name = typer.prompt("Please specify a nickname for this keystore")

        if len(keystore_config) > 0:
            for imported_keystore in keystore_config:
                if keystore_name == imported_keystore["keystore_name"]:
                    print(f"An imported keystore named {keystore_name} already exists.")
                    print("Exiting now...")
                    raise typer.Exit()

        # If there are no existing keystores, or if default keystore is not set, prompt user to choose whether to set keystore as default. # noqa 503
        if default_keystoreconfig is None:
            default_keystore_prompt = typer.confirm(
                f"There is no existing keystore. Would you like to make {keystore_name} the default keystore?"
            )
            if default_keystore_prompt:
                with open(cls.config_file_path, "r+", encoding="utf-8") as config_file_path:
                    cls._write_config("default_keystore", keystore_name)

        # Copy keystore to ~/.icon-cli/keystore
        cls._copy_file(f"{keystore_path}", f"{cls.config_dir_path}/keystore/{keystore_hash}.icx")

        # Create JSON payload to write to config.
        keystore_data = {
            "keystore_name": keystore_name,
            "keystore_address": keystore_address,
            "keystore_hash": keystore_hash,
            "keystore_filename": f"{keystore_hash}.icx",
        }

        # Write keystore name and address to config.json.
        with open(cls.config_file_path, "r+", encoding="utf-8") as config_file_path:
            config = yaml.full_load(config_file_path)
            config["keystores"].append(keystore_data)
            config_file_path.seek(0)
            yaml.dump(config, config_file_path, sort_keys=True)
            config_file_path.truncate()

        print("Keystore has been imported successfully.")

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

    @classmethod
    def _list_imported_keystore_names(cls):
        _config = cls._read_config()
        imported_keystores = _config["keystores"]
        if len(imported_keystores) > 0:
            keystore_names = [keystore["keystore_name"] for keystore in imported_keystores]
            return keystore_names
        else:
            print("There are no imported keystores.")
            raise typer.Exit()

    #############################
    # NETWORK-RELATED FUNCTIONS #
    #############################

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
    def inspect_config(cls):
        config = cls._read_config()
        return json.dumps(config, indent=4)

    ##############################
    # INTERNAL UTILITY FUNCTIONS #
    ##############################

    @classmethod
    def _copy_file(cls, source, destination):
        try:
            shutil.copyfile(source, destination)  # noqa 503
        except Exception as e:
            print(e)
            raise typer.Exit()

    @classmethod
    def _create_directory(cls, path):
        try:
            os.mkdir(path)
        except Exception as e:
            print(e)
            raise typer.Exit()
        else:
            print(f"config directory has been successfully created at {path}")

    @classmethod
    def _list_config_keys(cls) -> str:
        keys = list(cls.default_config.keys())
        return ", and ".join([", ".join(keys[:-1]), keys[-1]])

    @classmethod
    def _read_config(cls):
        with open(cls.config_file_path, "r") as config_file_path:
            config = yaml.full_load(config_file_path)
        return config

    @classmethod
    def _read_keystore(cls, keystore_path: PosixPath) -> tuple:
        with io.open(keystore_path, "r", encoding="utf-8-sig") as keystore_file:
            keystore_json = json.load(keystore_file)
            keystore_address = keystore_json["address"]
        keystore_hash = hashlib.md5(open(keystore_path, "rb").read()).hexdigest()
        return keystore_json, keystore_address, keystore_hash

    @classmethod
    def _write_config(cls, key: str, value: str):
        if not isinstance(value, str):
            print("Sorry, only string values are supported.")
            raise typer.Exit()
        if key in cls._list_config_keys():
            with open(cls.config_file_path, "r+", encoding="utf-8") as config_file_path:  # noqa 503
                config = yaml.full_load(config_file_path)
                config[key] = value
                config_file_path.seek(0)
                yaml.dump(config, config_file_path, sort_keys=True)
                config_file_path.truncate()
        else:
            print(f"Sorry, {key} is not a valid configuration key.")
            raise typer.Exit()
