import io
import json
import os
from pathlib import Path

import jsonschema
from yarl import URL

from icon_cli import ICX_KEYSTORE_JSON_SCHEMA, KEYSTORE_DIR
from icon_cli.contracts import Contracts
from icon_cli.utils import Utils


class Validators:
    def __init__(self) -> None:
        pass

    @staticmethod
    def validate_address(address: str) -> str:
        """
        Returns an ICX wallet or contract address if validation passes.

        Args:
            address: An ICX wallet or contract address.
        """
        try:
            # Convert address to lowercase.
            address = address.casefold()
            # Validate ICX wallet address.
            if len(address) == 42 and address[:2] in ("cx", "hx"):
                return address
            else:
                # Die if address is not validated successfully.
                raise ValueError
        except:
            # Die if address is not validated successfully.
            Utils.exit(f"{address} is not a valid ICX address.", "error")  # fmt: skip

    @staticmethod
    def validate_contract_address(address: str) -> str:
        try:
            address = address.casefold()
            if len(address) == 42 and address.startswith("cx"):
                return address
            elif address in Contracts.get_known_contract_names():
                return address
            else:
                raise ValueError
        except:
            Utils.exit(f"{address} is not a valid contract address.", "error")  # fmt: skip

    @staticmethod
    def validate_keystore_file(keystore_path: Path) -> Path:
        with io.open(keystore_path, "r", encoding="utf-8-sig") as keystore_file:
            keystore_data = json.load(keystore_file)
        try:
            jsonschema.validate(keystore_data, ICX_KEYSTORE_JSON_SCHEMA)
            return keystore_path
        except:
            # Die if address is not validated successfully.
            Utils.exit(f"{keystore_path} is not a valid ICX keystore file.", "error")

    @staticmethod
    def validate_keystore_name(keystore_name: str) -> str:
        """
        Returns the keystore name if its corresponding JSON file exists.

        Args:
            keystore_name: The name of the keystore to validate.
        """
        imported_keystores = os.listdir(KEYSTORE_DIR)
        if f"{keystore_name}.json" not in imported_keystores:
            Utils.exit(f"{keystore_name} is not a valid ICX keystore name.", "error")
        return keystore_name

    @staticmethod
    def validate_keystore_schema(keystore_data: dict) -> dict:
        """
        Returns the path of a keystore file if validation passes.

        Args:
            keystore_path: File path to an ICX keystore file.
        """

        try:
            jsonschema.validate(keystore_data, ICX_KEYSTORE_JSON_SCHEMA)
            return keystore_data
        except:
            # Die if address is not validated successfully.
            Utils.exit(f"ICX keystore is not valid.", "error")

    @staticmethod
    def validate_network(network: str) -> str:
        if network not in [
            "mainnet",
            "lisbon",
            "berlin",
            "sejong",
            "localhost",
        ]:
            Utils.exit(f"{network} is not a valid network.", "error")
        return network

    @staticmethod
    def validate_tx_hash(tx_hash: str) -> str:
        """
        Returns an ICX transaction hash if validation passes.

        Args:
            tx_hash: An ICX transaction hash.
        """
        # Convert transaction hash to lowercase.
        tx_hash = tx_hash.casefold()
        # Validate ICX transaction hash.
        if len(tx_hash) == 66 and tx_hash.startswith("0x"):
            return tx_hash
        else:
            # Die if address is not validated successfully.
            Utils.exit(f"{tx_hash} is not a valid ICX transaction hash.", "error")  # fmt: skip

    @staticmethod
    def validate_url(url: str) -> str:
        try:
            URL(url)
            return url
        except:
            Utils.exit(f"{url} is not a valid HTTP URL.", "error")
