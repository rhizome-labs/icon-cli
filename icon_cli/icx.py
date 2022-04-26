import requests
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

        self.network = network
        self.icon_service, self.nid = self._get_icon_service()

    def call(self, to, method, params=None):
        call = CallBuilder().to(to).method(method).params(params).build()
        result = self.icon_service.call(call)
        return result

    def get_balance(self, address: str):
        result = self.icon_service.get_balance(address)
        return result

    def get_contract_abi(self, contract: str):
        url = f"{self._get_tracker_endpoint()}/api/v1/contracts/{contract}"
        r = requests.get(url)
        data = r.json()
        abi = data["abi"]
        return abi

    def get_token_balance(self, address: str, contract: str):
        result = self.call(contract, "balanceOf", {"_owner": address})
        return int(result, 16)

    def _get_icon_service(self):
        try:
            network = self.default_networks[self.network]
            api_endpoint = network["api_endpoint"]
            nid = network["nid"]
            return (
                IconService(HTTPProvider(api_endpoint, self.API_VERSION)),
                nid,
            )
        except KeyError:
            print(f"ERROR: {network} is not a supported network.")
            raise typer.Exit()

    def _get_tracker_endpoint(self):
        network = self.default_networks[self.network]
        tracker_endpoint = network["tracker_endpoint"]
        return tracker_endpoint
