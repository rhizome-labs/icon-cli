from icon_cli.dapps.balanced.Balanced import Balanced


class BalancedDividends(Balanced):
    def __init__(self, network) -> None:
        super().__init__(network)

    ##################
    # CALL FUNCTIONS #
    ##################

    def distribution_check(self):
        result = self.call(self.BALANCED_DIVIDENDS_CONTRACT,
                           "distribute", None)
        return int(result, 16)

    def calculate_claim_in_usd(self, transaction_hash: str):
        transaction_result = self.icon_service.get_transaction_result(
            transaction_hash)
        return transaction_result

    #########################
    # TRANSACTION FUNCTIONS #
    #########################

    def distribute_dividends(self, wallet):
        transaction = self.build_call_transaction(
            wallet, self.BALANCED_DIVIDENDS_CONTRACT, "distribute", None
        )
        transaction_result = self.send_transaction(wallet, transaction)
        return transaction_result
