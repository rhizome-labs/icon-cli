import os
import typer
from dotenv import load_dotenv
from getpass import getpass
from iconsdk.exception import KeyStoreException
from iconsdk.wallet.wallet import KeyWallet
from icon_cli.models.Config import Config


class Identity(Config):
    def __init__(self) -> None:
        super().__init__()

    def load_wallet(self, keystore: str):
        try:
            load_dotenv()
            keystore_metadata = self.get_keystore_metadata(keystore)
            keystore_filename = keystore_metadata["keystore_filename"]
            keystore_name = keystore_metadata["keystore_name"]
            if os.getenv(keystore_name.upper()) is not None:
                wallet_password = os.getenv(keystore_name.upper())
            else:
                wallet_password = getpass("Keystore Password: ")
            wallet = KeyWallet.load(f"{self.keystore_dir}/{keystore_filename}", wallet_password)
            return wallet
        except KeyStoreException:
            print("Sorry, the password you supplied is incorrect.")
            raise typer.Exit()
        except Exception as e:
            print(e)
            raise typer.Exit()

    def get_wallet_address(self, keystore: str):
        try:
            wallet_address = self.get_keystore_metadata(keystore)["keystoreAddress"]
            return wallet_address
        except Exception as e:
            print(e)
            raise typer.Exit()
