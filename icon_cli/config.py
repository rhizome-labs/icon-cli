import io
import json
import os
import shutil
from pathlib import Path

import yaml

from icon_cli import CONFIG_FILE, KEYSTORE_DIR
from icon_cli.models import AppConfig


class Config:
    def __init__(self) -> None:
        pass

    @classmethod
    def get_default_keystore(cls) -> str:
        config = cls._read_config()
        default_keystore = config.default_keystore
        return default_keystore

    @classmethod
    def get_default_keystore_address(cls) -> str:
        default_keystore = cls.get_default_keystore()
        address = cls.get_keystore_public_key(f"{default_keystore}.json")
        return address

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
        with open(CONFIG_FILE, "w+") as f:
            yaml.safe_dump(config.dict(), f)
        return

    ####################
    # KEYSTORE METHODS #
    ####################

    @classmethod
    def get_imported_keystore_filenames(cls) -> list:
        files_in_keystore_dir = os.listdir(KEYSTORE_DIR)
        if len(files_in_keystore_dir) == 0:
            return []
        else:
            return files_in_keystore_dir

    @classmethod
    def get_imported_keystore_nicknames(cls) -> list:
        files_in_keystore_dir = os.listdir(KEYSTORE_DIR)
        if len(files_in_keystore_dir) == 0:
            return []
        else:
            return [
                os.path.splitext(keystore_filename)[0]
                for keystore_filename in files_in_keystore_dir
            ]

    @classmethod
    def get_keystore_public_key(cls, keystore_filename: Path) -> str:
        keystore_data = cls.read_keystore(f"{KEYSTORE_DIR}/{keystore_filename}")
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
        with open(CONFIG_FILE, "r") as f:
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
