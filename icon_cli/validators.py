import os
from getpass import getpass
from pathlib import PosixPath

from dotenv import load_dotenv
from iconsdk.exception import KeyStoreException
from iconsdk.wallet.wallet import KeyWallet

from icon_cli.config import Config
from icon_cli.tokens import Tokens
from icon_cli.utils import die


class Validators(Config):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def validate_address(cls, address: str):
        if address[:2] != "hx" or len(address) != 42:
            die(f"{address} is not a valid ICX address.", "error")
        return address

    @classmethod
    def validate_address_book_address_name(cls, name: str):
        config = Config.inspect_config()
        saved_addresses = config["saved_addresses"]
        if name not in saved_addresses:
            die(f"{name} does not exist in the address book.", "error")
        return name

    @classmethod
    def validate_contract(cls, contract):
        if contract is None:
            return contract
        elif contract[:2] != "cx" or len(contract) != 42:
            die(f"{contract} is not a valid ICX contract address.", "error")
        return contract

    @staticmethod
    def validate_keystore_file(keystore_path: PosixPath):
        valid_keystore_sizes = (509, 512)
        if keystore_path.stat().st_size not in valid_keystore_sizes:
            die(f"This keystore file is not valid.", "error")
        return keystore_path

    @classmethod
    def validate_lowercase_only(cls, input: str):
        return input.lower()

    @classmethod
    def validate_network(cls, network: str):
        if network not in cls.default_networks.keys():
            die(f"{network} is not a valid network.", "error")
        return network

    @classmethod
    def validate_token(cls, token: str):
        if token is None:
            return token
        if token[:2] == "cx" or len(token) == 42:  # Token contract
            return token
        else:
            try:
                token_contract = Tokens.get_contract_from_ticker(token.upper())
                return token_contract
            except KeyError:
                die(f"{token} is not a supported token.", "error")

    @classmethod
    def validate_transaction_value(cls, value: str):
        try:
            return float(value)
        except ValueError:
            die(f"{value} is not a valid transaction value.", "error")

    @classmethod
    def validate_uppercase_only(cls, input: str):
        return input.upper()

    @classmethod
    def validate_token_ticker(cls, ticker):
        valid_tokens = Tokens.TOKENS.keys()
        if ticker not in valid_tokens:
            die(f"{ticker} is not supported at this time.", "error")
        return ticker.upper()

    @classmethod
    def load_wallet_from_keystore(cls, keystore):
        try:
            keystore_metadata = Config.get_keystore_metadata(keystore)
            keystore_filename = keystore_metadata["keystore_filename"]
            keystore_name = keystore_metadata["keystore_name"]
            if os.getenv(keystore_name.upper()):
                wallet_password = os.getenv(keystore_name.upper())
            else:
                wallet_password = getpass("Keystore Password: ")
            wallet = KeyWallet.load(
                f"{Config.keystore_dir}/{keystore_filename}", wallet_password
            )
            return wallet
        except KeyStoreException:
            die("The password you supplied is incorrect.", "error")
        except Exception as e:
            die(e, "error")
