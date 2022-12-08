from functools import lru_cache

from iconsdk.builder.call_builder import CallBuilder
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.wallet.wallet import KeyWallet

from icon_cli.config import Config


class Icx(Config):

    API_VERSION = 3

    def __init__(self, network) -> None:
        super().__init__()

        self.network = network
        self.icon_service, self.nid = self._get_icon_service_and_nid()

    def call(
        self,
        to: str,
        method: str,
        params: dict = {},
        height: int = None,
    ):
        call = CallBuilder().to(to).method(method).params(params).height(height).build()
        result = self.icon_service.call(call)
        return result

    ##########################
    # Built-In Query Methods #
    ##########################

    def get_block(
        self,
        block_height: int = "latest",
    ) -> dict:
        """
        Returns information about a specific block on the ICON blockchain.

        Args:
            block_height: The block height to query.
        """
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

    def create_keystore():
        wallet = wallet

    ######################
    # Common Query Calls #
    ######################

    @lru_cache(maxsize=128)
    def get_icx_usd_price(self, block_height: int = None) -> float:
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
    ):
        """
        Parses configuration and returns an IconService object and ICON network ID.

        Args:
            network: Name of the network (e.g. "mainnet").
        """
        # Get IcxNetwork object with network details.
        _network = self.DEFAULT_NETWORKS[network]
        # Get API endpoint and network ID from IcxNetwork object.
        api_endpoint = _network.api_endpoint
        nid = _network.nid
        icon_service = IconService(HTTPProvider(api_endpoint, self.API_VERSION))
        return icon_service, nid
