import os
import requests
import typer
from iconsdk.builder.call_builder import CallBuilder
from iconsdk.builder.transaction_builder import (
    CallTransactionBuilder,
    DeployTransactionBuilder,
    MessageTransactionBuilder,
    TransactionBuilder,
)
from iconsdk.exception import JSONRPCException, KeyStoreException
from iconsdk.icon_service import IconService
from iconsdk.wallet.wallet import KeyWallet
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.signed_transaction import SignedTransaction
from icon_cli.models.Config import Config
from dotenv import load_dotenv
from getpass import getpass
from random import randint
from time import sleep


class Icx:

    ICX_GOVERNANCE_CONTRACT = "cx0000000000000000000000000000000000000000"

    def __init__(self, network) -> None:

        self.network = network
        self.api_version = 3
        self.icon_service, self.nid = self._get_icon_service(self.network)
        self.tracker_endpoint = self._get_tracker_url(self.network)

    ###################
    # CALL PRIMITIVES #
    ###################

    def call(self, to, method, params=None):
        try:
            call = CallBuilder().to(to).method(method).params(params).build()
            result = self.icon_service.call(call)
            return result
        except JSONRPCException as e:
            print(e)
            raise typer.Exit()

    ##################
    # CALL FUNCTIONS #
    ##################

    def query_latest_block(self):
        latest_block = self.icon_service.get_block("latest")
        return latest_block

    def query_block(self, block: int):
        block = self.icon_service.get_block(block)
        return block

    def query_token_balance(self, address, ticker: str):
        tickers = Config.irc2_token_tickers
        contract_address = tickers[ticker.upper()]
        token_balance = self.call(contract_address, "balanceOf", {"_owner": address})
        return int(token_balance, 16) / 10 ** 18

    def query_transaction_result(self, transaction_hash: str):
        transaction_result = self.icon_service.get_transaction_result(transaction_hash)  # noqa 503
        transaction_result.pop("logsBloom")
        return transaction_result

    #####################
    # TRACKER FUNCTIONS #
    #####################

    def query_address_info(self, address: str) -> dict:
        response = self._make_tracker_request(f"/address/info?address={address}")  # noqa 503
        return response

    def query_icx_supply(self) -> dict:
        response = self._make_tracker_request("/main/mainInfo")  # noqa 503
        return response

    ##########################
    # TRANSACTION PRIMITIVES #
    ##########################

    def build_transaction(self, wallet, to, value):
        try:
            transaction = (
                TransactionBuilder()
                .from_(wallet.get_address())
                .to(to)
                .value(value * 10 ** 18)
                .nid(self.nid)
                .nonce(self._generate_nonce())
                .build()
            )
            return transaction
        except Exception as e:
            print(e)
            raise typer.Exit()

    def build_call_transaction(self, wallet, to, method, params: dict = {}):
        try:
            transaction = (
                CallTransactionBuilder()
                .from_(wallet.get_address())
                .to(to)
                .nid(self.nid)
                .nonce(self._generate_nonce())
                .method(method)
                .params(params)
                .build()
            )
            return transaction
        except Exception as e:
            print(e)
            raise typer.Exit()

    def build_deploy_transaction(self, wallet, to, content, params):
        try:
            transaction = (
                DeployTransactionBuilder()
                .from_(wallet.get_address())
                .to(to)
                .nid(self.nid)
                .nonce(self._generate_nonce())
                .content_type("application/zip")
                .content(content)
                .params(params)
                .build()
            )
            return transaction
        except Exception as e:
            print(e)
            raise typer.Exit()

    def build_message_transaction(self, wallet, to, data):
        try:
            transaction = (
                MessageTransactionBuilder()
                .from_(wallet.get_address())
                .to(to)
                .nid(self.nid)
                .nonce(self._generate_nonce())
                .data(data)
                .build()
            )
            return transaction
        except Exception as e:
            print(e)
            raise typer.Exit()

    def send_transaction(self, wallet, transaction):
        try:
            step_limit = self.icon_service.estimate_step(transaction) + 1000
            signed_transaction = SignedTransaction(transaction, wallet, step_limit)
            transaction_hash = self.icon_service.send_transaction(signed_transaction)
            transaction_result = self._get_transaction_result(transaction_hash)
            return transaction_result
        except Exception as e:
            print(e)
            raise typer.Exit()

    ####################
    # WALLET FUNCTIONS #
    ####################

    def load_wallet(self, keystore: str):
        try:
            load_dotenv()
            keystore_metadata = Config.get_keystore_metadata(keystore)
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

    ##############################
    # INTERNAL UTILITY FUNCTIONS #
    ##############################

    def _generate_nonce(self, length=8):
        nonce = int("".join([str(randint(0, 9)) for i in range(length)]))  # noqa 503
        return nonce

    def _get_icon_service(self, network: str):
        default_networks = Config.get_default_networks()
        endpoint_hostname, nid = default_networks.get(network)
        return (
            IconService(HTTPProvider(endpoint_hostname, self.api_version)),
            nid,
        )

    def _get_tracker_url(self, network: str):
        if network == "mainnet":
            return "https://tracker.icon.foundation/v3"
        else:
            print("This command is only supported on mainnet.")
            raise typer.Exit()

    def _make_tracker_request(self, url):
        try:
            response = requests.get(f"{self.tracker_endpoint}{url}")
            response.raise_for_status()
            return response.json()["tmainInfo"]
        except Exception as e:
            print(e)
            raise typer.Exit()

    def _get_transaction_result(self, transaction_hash):
        while True:
            try:
                transaction_result = self.icon_service.get_transaction_result(transaction_hash)
                if transaction_result["status"] == 1:
                    break
            except JSONRPCException:
                typer.echo("Transaction in progress...")
                sleep(1)
                continue
        return transaction_result
