import typer
from dotenv import load_dotenv
from iconsdk.builder.call_builder import CallBuilder
from iconsdk.builder.transaction_builder import (
    CallTransactionBuilder,
    DeployTransactionBuilder,
    MessageTransactionBuilder,
    TransactionBuilder,
)
from iconsdk.exception import JSONRPCException, KeyStoreException
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.wallet.wallet import KeyWallet
from rich import print
from rich.console import Console

from icon_cli.config import Config


class Icx(Config):

    API_VERSION = 3

    def __init__(self, network) -> None:
        super().__init__()

        self.icon_service, self.nid = self._get_icon_service(network)

    def call(self, to, method, params=None):
        try:
            call = CallBuilder().to(to).method(method).params(params).build()
            result = self.icon_service.call(call)
            return result
        except JSONRPCException:
            raise typer.Exit()

    def get_balance(self, address: str):
        try:
            result = self.icon_service.get_balance(address)
            return result
        except JSONRPCException:
            raise typer.Exit()

    def get_token_balance(self, address: str, contract: str):
        try:
            result = self.call(contract, "balanceOf", {"_owner": address})
            return int(result, 16)
        except JSONRPCException:
            raise typer.Exit()

    def _get_icon_service(self, network: str = None):
        try:
            network = self.default_networks[network]
            api_endpoint = network["api_endpoint"]
            nid = network["nid"]
            return (
                IconService(HTTPProvider(api_endpoint, self.API_VERSION)),
                nid,
            )
        except KeyError:
            print(f"ERROR: {network} is not a supported network.")
            raise typer.Exit()
