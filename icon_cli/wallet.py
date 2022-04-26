from pathlib import PosixPath

from dotenv import load_dotenv
from iconsdk.wallet.wallet import KeyWallet

from icon_cli.config import Config


class Wallet(Config):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def load_wallet(cls, wallet_path: PosixPath, password: str):
        wallet = KeyWallet.load(wallet_path, password)
        return wallet

    @classmethod
    def create_wallet(cls, password: str):
        wallet = KeyWallet.create()
        wallet.store(cls.keystore_dir, password)
        return wallet
