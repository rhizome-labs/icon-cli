import json
import token_contracts
from icon_cli.dapps.balanced.Balanced import Balanced 

class BalancedDex(Balanced):
    def __init__(self, network) -> None:
        super().__init__(network)

    #########################
    # TRANSACTION FUNCTIONS #
    #########################

    def swap(self, wallet, amount: int, from_token: str, to_token: str, slippage: str, minimum_receive: int):
        from_token_contract = token_contracts[from_token.upper()]
        to_token_contract = token_contracts[to_token.upper()]
        swap_data = {
            "method": "_swap",
            "params": {
                "toToken": to_token_contract,
                "minimumReceive": minimum_receive
            }
        }
        params = {
            "_to": self.BALANCED_DEX_CONTRACT,
            "_value": amount,
            "_data": str.encode(json.dumps(swap_data)),
        }
        transaction = self.build_call_transaction(
            wallet, from_token_contract, "transfer", params
        )
        transaction_result = self.send_transaction(wallet, transaction)
        return transaction_result


