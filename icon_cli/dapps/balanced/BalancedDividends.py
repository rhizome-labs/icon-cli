from icon_cli.dapps.balanced.Balanced import Balanced


class BalancedDividends(Balanced):
    def __init__(self, network) -> None:
        super().__init__(network)

    ##################
    # CALL FUNCTIONS #
    ##################

    def distribution_check(self):
        result = self.call(self.BALANCED_DIVIDENDS_CONTRACT, "distribute", None)
        return int(result, 16)

    #########################
    # TRANSACTION FUNCTIONS #
    #########################

    def distribute_dividends(self, wallet):
        transaction = self.build_call_transaction(
            wallet, self.BALANCED_DIVIDENDS_CONTRACT, "distribute", None
        )
        transaction_result = self.send_transaction(wallet, transaction)
        return transaction_result