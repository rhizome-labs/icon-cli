from icon_cli.icx import Icx
from icon_cli.utils import die


class Cps(Icx):
    def __init__(self, network) -> None:
        super().__init__(network)

        if network != "mainnet":
            die("This command only supports mainnet at this time.", "error")

    def get_proposals():
        pass
