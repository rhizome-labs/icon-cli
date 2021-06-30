import typer
from getpass import getpass
from iconsdk.exception import KeyStoreException
from iconsdk.wallet.wallet import KeyWallet
from icon_cli.models.Config import Config


class Identity(Config):

    config = Config()

    def __init__(self) -> None:
        super().__init__()

    def load_wallet(self, keystore: str):
        try:
            keystore_metadata = self.get_keystore_metadata(keystore)
            print(keystore_metadata)
            keystore_filename = keystore_metadata["keystore_filename"]
            print(keystore_filename)
            # wallet_password = getpass("Keystore Password: ")
            wallet_password = "alskALSK123~~"
            wallet = KeyWallet.load(f"{self.keystore_dir_path}/{keystore_filename}", wallet_password)
            return wallet
        except KeyStoreException:
            print("Sorry, the password you supplied is incorrect.")
            raise typer.Exit()
        except Exception as e:
            print(e)
            raise typer.Exit()

    @classmethod
    def get_wallet_address(cls, keystore: str):
        try:
            wallet_address = cls.get_keystore_metadata(keystore)["keystoreAddress"]
            return wallet_address
        except Exception as e:
            print(e)
            raise typer.Exit()
