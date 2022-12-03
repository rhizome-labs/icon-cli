from icon_cli.dapps.balanced.Balanced import Balanced


class BalancedGovernance(Balanced):
    def __init__(self, network) -> None:
        super().__init__(network)

    #########################
    # TRANSACTION FUNCTIONS #
    #########################

    def evaluate_vote(self, wallet, vote_index: int):
        params = {"vote_index": vote_index}
        transaction = self.build_call_transaction(
            wallet, self.BALANCED_GOVERNANCE_CONTRACT, 0, "evaluateVote", params
        )
        transaction_result = self.send_transaction(wallet, transaction)
        return transaction_result

    def execute_vote(self, wallet, vote_index: int):
        params = {"vote_index": vote_index}
        transaction = self.build_call_transaction(
            wallet, self.BALANCED_GOVERNANCE_CONTRACT, 0, "executeVoteAction", params
        )
        transaction_result = self.send_transaction(wallet, transaction)
        return transaction_result
