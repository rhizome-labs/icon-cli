from pathlib import PosixPath

from icon_cli.config import Config
from icon_cli.tokens import Tokens
from icon_cli.utils import die


class Validators(Config):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def validate_address(cls, address):
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
    def validate_keystore(keystore_path: PosixPath):
        valid_keystore_sizes = (509, 512)
        if keystore_path.stat().st_size not in valid_keystore_sizes:
            die(f"This keystore file is not valid.", "error")
        return keystore_path

    @classmethod
    def validate_lowercase_only(cls, input: str):
        return input.lower()

    @classmethod
    def validate_network(cls, network):
        if network not in cls.default_networks.keys():
            die(f"{network} is not a valid network.", "error")
        return network

    @classmethod
    def validate_uppercase_only(cls, input: str):
        return input.upper()

    @staticmethod
    def validate_token_ticker(ticker):
        valid_tokens = Tokens.TOKENS.keys()
        if ticker not in valid_tokens:
            die(f"{ticker} is not supported at this time.", "error")
        return ticker.upper()
