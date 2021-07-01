import os
import typer
from dotenv import load_dotenv
from getpass import getpass
from iconsdk.exception import KeyStoreException
from iconsdk.wallet.wallet import KeyWallet
from icon_cli.models.Config import Config
from pathlib import PosixPath


class Callbacks:
    def __init__(self) -> None:
        pass

    @staticmethod
    def enforce_mainnet(network):
        if network != "mainnet":
            print(f"Sorry, this command is only available on mainnet. Your network is currently set to {network}.")
            raise typer.Exit()
        else:
            return network

    @staticmethod
    def load_wallet_from_keystore(keystore_name: str):
        imported_keystores = Config.list_imported_keystore_names()
        if keystore_name in imported_keystores:
            try:
                load_dotenv()
                keystore_metadata = Config.get_keystore_metadata(keystore_name)
                keystore_filename = keystore_metadata["keystore_filename"]
                keystore_name = keystore_metadata["keystore_name"]
                if os.getenv(keystore_name.upper()) is not None:
                    wallet_password = os.getenv(keystore_name.upper())
                else:
                    wallet_password = getpass("Keystore Password: ")
                wallet = KeyWallet.load(f"{Config.keystore_dir}/{keystore_filename}", wallet_password)
                return wallet
            except KeyStoreException:
                print("Sorry, the password you supplied is incorrect.")
                raise typer.Exit()
            except Exception as e:
                print(e)
                raise typer.Exit()
        else:
            print(f"Sorry, {keystore_name} is not a valid keystore.")
            raise typer.Exit()

    @staticmethod
    def validate_block(block: int):
        if block == 0:
            return "latest"
        if block >= 1:
            return block
        else:
            print("Sorry, block height must be greater than 1.")
            raise typer.Exit()

    @staticmethod
    def validate_icx_address(address: str):
        if address[:2] in ["hx", "cx"] and len(address) == 42:
            return address
        else:
            print(f"Sorry, {address} is not a valid ICX address.")
            raise typer.Exit()

    @staticmethod
    def validate_keystore_name(keystore_name: str):
        imported_keystores = Config.list_imported_keystore_names()
        if keystore_name in imported_keystores:
            return keystore_name
        else:
            print(f"Sorry, {keystore_name} is not a valid keystore.")
            raise typer.Exit()

    @staticmethod
    def validate_keystore_integrity(keystore_path: PosixPath):
        if keystore_path.stat().st_size == 512:  # noqa 503
            return keystore_path
        else:
            print(f"{keystore_path} is not a valid keystore file.")
            raise typer.Exit()

    @staticmethod
    def validate_network(network: str):
        if network in Config.get_default_networks():
            return network
        else:
            print(f"Sorry, {network} is not a valid network.")
            raise typer.Exit()

    @staticmethod
    def validate_output_format(format):
        if format != "json":
            format = "default"
        return format
