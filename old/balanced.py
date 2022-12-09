from icon_cli.contracts import Contracts
from icon_cli.icx import Icx
from icon_cli.tokens import Tokens
from icon_cli.utils import die


class Balanced(Icx):
    def __init__(self, network) -> None:
        super().__init__(network)

        if network != "mainnet":
            exit("This command only supports mainnet at this time.", "error")

    ##########################
    # BALANCED PEG STABILITY #
    ##########################

    def send_to_stability_fund(self, wallet, token, value):
        print(token)
        # contract = Tokens.get_contract_from_ticker(token)
        # tx_hash = self.transfer_token(
        #    wallet,
        #    Contracts.get_contract_from_name("balanced_stability_fund"),
        #    contract,
        #    value,
        #    Tokens.get_token_precision_from_contract(contract),
        # )
