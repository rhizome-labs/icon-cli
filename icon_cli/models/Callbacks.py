import typer
from icon_cli.models.Config import Config
from icon_cli.models.Identity import Identity


class Callbacks:
    def __init__(self) -> None:
        self.config = Config()
        self.identity = Identity()

    @classmethod
    def convert_keystore_to_wallet(self, keystore_name: str):
        imported_keystores = self.config._list_imported_keystore_names()
        if keystore_name in imported_keystores:
            wallet = self.identity.load_wallet(keystore_name)
            return wallet
        else:
            print(f"Sorry, {keystore_name} is not a valid keystore.")
            raise typer.Exit()
