import io
import json
import os
from pathlib import Path, PosixPath

import jsonschema
import typer
from yarl import URL


class Utils:

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

    def __init__(self) -> None:
        pass

    @classmethod
    def abs_path(cls, relative_path: str) -> Path:
        """
        A function that converts a relative path to an absolute path.
        """
        return os.path.abspath(relative_path)

    @classmethod
    def exit(cls, message: str, level: str = None):
        """
        A function that formats and prints an error message before exiting the program.
        """
        # Set color and prefix for die message.
        if level == "error":
            fg = "red"
            prefix = "ERROR: "
        elif level == "warning":
            fg = "orange"
            prefix = "WARNING: "
        elif level == "ok":
            fg = "green"
            prefix = "OK: "
        elif level == "success":
            fg = "green"
            prefix = "SUCCESS: "
        else:
            fg = None
            prefix = None

        # Print die message.
        typer.secho(f"{prefix}{message}", fg=fg)

        # Exit application.
        raise typer.Exit()

    @classmethod
    def strip_all_whitespace(cls, input: str, force_lowercase: bool):
        """
        A function that strips all whitespace from a string.
        """
        input = input.strip()
        input = input.replace(" ", "")
        # Convert to lowercase if force_lowercase is True.
        if force_lowercase is True:
            input = input.casefold()
        return input

    ###################
    # DATA VALIDATORS #
    ###################

    @classmethod
    def validate_address(cls, address: str) -> str:
        """
        Returns an ICX wallet or contract address if validation passes.

        Args:
            address: An ICX wallet or contract address.
        """
        try:
            # Convert address to lowercase.
            address = address.casefold()
            # Validate ICX wallet address.
            if len(address) == 42 and address.startswith("hx"):
                return address
            # Validate ICX contract address.
            elif len(address) == 42 and address.startswith("cx"):
                return address
            else:
                # Die if address is not validated successfully.
                Utils.exit(f"{address} is not a valid ICX wallet or contract address.", "error")  # fmt: skip
        except:
            # Die if address is not validated successfully.
            Utils.exit(f"{address} is not a valid ICX wallet or contract address.", "error")  # fmt: skip

    @classmethod
    def validate_keystore_file(cls, keystore_path: PosixPath):
        with io.open(keystore_path, "r", encoding="utf-8-sig") as keystore_file:
            keystore_data = json.load(keystore_file)
        try:
            jsonschema.validate(keystore_data, cls.ICX_KEYSTORE_JSON_SCHEMA)
            return keystore_path
        except:
            # Die if address is not validated successfully.
            Utils.exit(f"{keystore_path} is not a valid ICX keystore file.", "error")

    @classmethod
    def validate_keystore_schema(cls, keystore_data: dict) -> dict:
        """
        Returns the path of a keystore file if validation passes.

        Args:
            keystore_path: File path to an ICX keystore file.
        """

        try:
            jsonschema.validate(keystore_data, cls.ICX_KEYSTORE_JSON_SCHEMA)
            return keystore_data
        except:
            # Die if address is not validated successfully.
            Utils.exit(f"ICX keystore is not valid.", "error")

    @classmethod
    def validate_tx_hash(cls, tx_hash: str) -> str:
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

    @classmethod
    def validate_url(cls, url: str) -> str:
        try:
            URL(url)
            return url
        except:
            Utils.exit(f"{url} is not a valid HTTP URL.", "error")
