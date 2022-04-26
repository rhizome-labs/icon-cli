from icon_cli.icx import Icx
from icon_cli.utils import hex_to_int


class Gov(Icx):
    def __init__(self, network) -> None:
        super().__init__(network)

    def query_delegation(self, address):
        params = {"address": address}
        result = self.call(self.GOVERNANCE_CONTRACT, "getDelegation", params)

        for k, v in result.items():
            if isinstance(v, str) and v[:2] == "0x":
                result[k] = hex_to_int(v, 18)

        if len(result["delegations"]) > 0:
            delegations = result["delegations"]
            for delegation in delegations:
                delegation["value"] = hex_to_int(delegation["value"], 18)

        return result

    def set_bonder_list(self, bonder_list, wallet):
        params = {"bonderList": bonder_list}
        tx = self.build_call_transaction(
            wallet, self.CHAIN_CONTRACT, 0, "setBonderList", params
        )
        tx_hash = self.send_transaction(wallet, tx)
        return tx_hash
