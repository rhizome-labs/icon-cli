from getpass import getpass
from random import randint

import requests
import typer
from iconsdk.builder.call_builder import CallBuilder
from iconsdk.builder.transaction_builder import (
    CallTransactionBuilder,
    TransactionBuilder,
)
from iconsdk.exception import KeyStoreException
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.signed_transaction import SignedTransaction
from iconsdk.wallet.wallet import KeyWallet

from icon_cli.config import Config
from icon_cli.utils import die


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

    ##########################
    # TRANSACTION PRIMITIVES #
    ##########################

    def build_transaction(self, wallet, to, value):
        transaction = (
            TransactionBuilder()
            .from_(wallet.get_address())
            .to(to)
            .value(value)
            .nid(self.nid)
            .nonce(self._generate_nonce())
            .build()
        )
        return transaction

    def build_call_transaction(
        self, wallet, to, value: int = 0, method: str = None, params: dict = None
    ):
        transaction = (
            CallTransactionBuilder()
            .from_(wallet.get_address())
            .to(to)
            .value(value)
            .nid(self.nid)
            .nonce(self._generate_nonce())
            .method(method)
            .params(params)
            .build()
        )
        return transaction

    def send_transaction(self, wallet, transaction):
        try:
            step_limit = self.icon_service.estimate_step(transaction) + 100000
            signed_transaction = SignedTransaction(transaction, wallet, int(step_limit))
            tx_hash = self.icon_service.send_transaction(signed_transaction)
            return tx_hash
        except Exception as e:
            die(e, "error")

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

    #########################
    # TRANSACTION FUNCTIONS #
    #########################

    def transfer_token(
        self,
        wallet,
        to_address: str,
        token_contract: str,
        value: float,
        token_precision: int,
    ):
        params = {"_to": to_address, "_value": value * 10**token_precision}
        transaction = self.build_call_transaction(
            wallet, token_contract, 0, "transfer", params
        )
        tx_hash = self.send_transaction(transaction)
        return tx_hash

    ####################
    # WALLET FUNCTIONS #
    ####################

    @classmethod
    def load_wallet(cls, keystore: str):
        try:
            keystore_metadata = Config.get_keystore_metadata(keystore)
            keystore_filename = keystore_metadata["keystore_filename"]
            wallet_password = getpass("Keystore Password: ")
            wallet = KeyWallet.load(
                f"{Config.keystore_dir}/{keystore_filename}", wallet_password
            )
            return wallet
        except KeyStoreException:
            die("The password you supplied is incorrect.", "error")
        except Exception as e:
            die(e, "error")

    ##############################
    # INTERNAL UTILITY FUNCTIONS #
    ##############################

    def _generate_nonce(self, length=6):
        nonce = int("".join([str(randint(0, 9)) for i in range(length)]))  # noqa 503
        return nonce
