import typer
from rich import inspect

from icon_cli.config import Config
from icon_cli.tokens import Tokens
from icon_cli.utils import die


class Validators(Config):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def validate_network(cls, network):
        if network not in cls.default_networks.keys():
            die(f"{network} is not a valid network.", "error")
        return network

    @classmethod
    def validate_address(cls, address):
        if address[:2] != "hx" or len(address) != 42:
            die(f"{address} is not a valid ICX address.", "error")
        return address

    @classmethod
    def validate_contract(cls, contract):
        if contract is None:
            return contract
        elif contract[:2] != "cx" or len(contract) != 42:
            die(f"{contract} is not a valid ICX contract address.", "error")
        return contract

    @staticmethod
    def validate_token_ticker(ticker):
        valid_tokens = Tokens.TOKENS.keys()
        if ticker not in valid_tokens:
            die(f"{ticker} is not supported at this time.", "error")
        return ticker.upper()
