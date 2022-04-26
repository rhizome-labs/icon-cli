from icon_cli.dapps.balanced.Balanced import Balanced


class BalancedRouter(Balanced):
    def __init__(self, network) -> None:
        super().__init__(network)

    #########################
    # TRANSACTION FUNCTIONS #
    #########################

    def route(self, path):
        pass