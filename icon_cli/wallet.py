from getpass import getpass

from iconsdk.exception import KeyStoreException
from iconsdk.wallet.wallet import KeyWallet

from icon_cli.config import Config
from icon_cli.utils import die


class Wallet(Config):
    def __init__(self) -> None:
        super().__init__()

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

    @classmethod
    def create_wallet(cls, password: str):
        wallet = KeyWallet.create()
        wallet.store(cls.keystore_dir, password)
        return wallet
