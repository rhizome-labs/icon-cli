from iconsdk.wallet.wallet import KeyWallet

from icon_cli.config import Config


class Icx(Config):

    API_VERSION = 3

    def __init__(self, network) -> None:
        super().__init__()

        self.network = network
        self.icon_service, self.nid = self._get_icon_service()

    def create_keystore():
        wallet = wallet

    def _get_icon_service(self, network):

        return
