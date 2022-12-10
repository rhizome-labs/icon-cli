from decimal import Decimal
from functools import lru_cache
from getpass import getpass
from typing import Tuple

from iconsdk.builder.call_builder import CallBuilder
from iconsdk.builder.transaction_builder import (
    CallTransactionBuilder,
    TransactionBuilder,
)
from iconsdk.exception import JSONRPCException, KeyStoreException
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.signed_transaction import SignedTransaction, Transaction
from iconsdk.wallet.wallet import KeyWallet

from icon_cli import DEFAULT_NETWORKS, EXA, KEYSTORE_DIR
from icon_cli.config import Config
from icon_cli.tokens import Tokens
from icon_cli.utils import Utils


class Icx(Config):

    API_VERSION = 3

    def __init__(
        self,
        network,
        keystore_name: str = None,
        keystore_password: str = None,
    ) -> None:
        super().__init__()
        self.network = network
        self.icon_service, self.nid = self._get_icon_service_and_nid(self.network)

        if keystore_name is not None:
            self.keystore_name = keystore_name
            self.keystore_password = keystore_password
            self.wallet = self._load_keystore(self.keystore_name, self.keystore_password)  # fmt: skip
            self.wallet_address = self.wallet.get_address()

    def call(
        self,
        to: str,
        method: str,
        params: dict = {},
        height: int = None,
    ) -> dict:
        call = CallBuilder().to(to).method(method).params(params).height(height).build()
        result = self.icon_service.call(call)
        return result

    ##########################
    # Built-In Query Methods #
    ##########################

    def get_balance(
        self,
        address: str,
        in_loop: bool = False,
    ) -> int | Decimal:
        balance = self.icon_service.get_balance(address)
        if in_loop is True:
            return balance
        else:
            return Decimal(balance) / EXA

    def get_block(
        self,
        block_height: int = -1,
    ) -> dict:
        """
        Returns information about a specific block on the ICON blockchain.

        Args:
            block_height: The block height to query.
        """
        if block_height == -1:
            block_height = "latest"
        result = self.icon_service.get_block(block_height)
        return result

    def get_score_api(
        self,
        contract_address: str,
        block_height: int = None,
    ) -> dict:
        """
        Returns the ABI for a SCORE on the ICON blockchain.

        Args:
            contract_address: The contract to get the ABI for.
            block_height: The block height to query.
        """
        result = self.icon_service.get_score_api(contract_address, block_height)
        return result

    def get_token_balance(
        self,
        address: str,
        token_symbol: str,
        network: str,
        in_loop: bool = False,
    ) -> int | Decimal:
        token = Tokens.get_token(token_symbol).dict()
        params = {"_owner": address}
        result = self.call(token[network], "balanceOf", params)
        token_balance = Utils.to_int(result)
        if in_loop is True:
            return token_balance
        else:
            return Decimal(token_balance) / EXA

    def get_transaction(
        self,
        tx_hash: str,
    ) -> dict:
        """
        Returns details of a transaction on the ICON blockchain.

        Args:
            tx_hash: An ICX transaction hash.
        """
        result = self.icon_service.get_transaction(tx_hash)
        return result

    def get_transaction_result(
        self,
        tx_hash: str,
    ) -> dict:
        """
        Returns the result of a transaction on the ICON blockchain.

        Args:
            tx_hash: An ICX transaction hash.
        """
        result = self.icon_service.get_transaction_result(tx_hash)
        return result

    ######################
    # Common Query Calls #
    ######################

    @lru_cache(maxsize=128)
    def get_icx_usd_price(
        self,
        block_height: int = None,
    ) -> float:
        """
        Returns a quote for ICX/USD from the Band oracle.

        Args:
            block_height: The block height to query.
        """
        params = {"_symbol": "ICX"}
        result = self.call(
            "cx087b4164a87fdfb7b714f3bafe9dfb050fd6b132",
            "get_ref_data",
            params,
            height=block_height,
        )
        icx_usd_price = int(result["rate"], 16) / 1_000_000_000
        return icx_usd_price

    @lru_cache(maxsize=1)
    def _get_icon_service_and_nid(
        self,
        network,
    ) -> Tuple[IconService, int]:
        """
        Parses configuration and returns an IconService object and ICON network ID.

        Args:
            network: Name of the network (e.g. "mainnet").
        """
        # Get IcxNetwork object with network details.
        _network = DEFAULT_NETWORKS[network]
        # Get API endpoint and network ID from IcxNetwork object.
        api_endpoint = _network.api_endpoint
        nid = _network.nid
        icon_service = IconService(HTTPProvider(api_endpoint, self.API_VERSION))
        return icon_service, nid

    ########################
    # TRANSACTION BUILDERS #
    ########################

    def build_transaction(
        self,
        to: str,
        value: int,
    ) -> Transaction:
        tx = (
            TransactionBuilder()
            .from_(self.wallet_address)
            .to(to)
            .value(int(value * EXA))
            .nid(self.nid)
            .build()
        )
        return tx

    def build_call_transaction(
        self,
        to: str,
        value: int = 0,
        method: str = None,
        params: dict = {},
    ):
        transaction = (
            CallTransactionBuilder()
            .from_(self.wallet_address)
            .to(to)
            .value(int(value))
            .nid(self.nid)
            .method(method)
            .params(params)
            .build()
        )
        return transaction

    def send_transaction(self, tx: Transaction) -> str:
        signed_tx = SignedTransaction(tx, self.wallet, 100_000_000)
        tx_hash = self.icon_service.send_transaction(signed_tx)
        return tx_hash

    def is_transaction_successful(self, tx_hash: str) -> bool:
        tx_result = self.icon_service.get_transaction_result(tx_hash)
        return

    ##################
    # Wallet Methods #
    ##################

    def _load_keystore(
        self,
        keystore_name: str,
        keystore_password: str,
    ) -> KeyWallet:
        try:
            # Prompt user for keystore password if it's not provided.
            if keystore_password is None:
                keystore_password = getpass("Keystore Password: ")
            # Load keystore.
            keystore = KeyWallet.load(
                f"{KEYSTORE_DIR}/{keystore_name}.json",
                keystore_password,
            )
            return keystore
        except KeyStoreException:
            Utils.exit("The password you supplied is incorrect.", "error")
