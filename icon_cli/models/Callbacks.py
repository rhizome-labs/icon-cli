import typer
from icon_cli.models.Config import Config
from icon_cli.models.Identity import Identity


class Callbacks:

    config = Config()
    identity = Identity()

    @classmethod
    def convert_keystore_to_wallet(cls, keystore_name: str):
        imported_keystores = cls.config._list_imported_keystore_names()
        if keystore_name in imported_keystores:
            wallet = cls.identity.load_wallet(keystore_name)
            return wallet
        else:
            print(f"Sorry, {keystore_name} is not a valid keystore.")
            raise typer.Exit()
