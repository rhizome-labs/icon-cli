from icon_cli.utils import hex_to_int
from icon_cli.icx import Icx


class Gov(Icx):
    def __init__(self, network) -> None:
        super().__init__(network)

    def query_delegation(self, address):
        params = {"address": address}
        result = self.call(self.ICX_GOVERNANCE_CONTRACT_0,
                           "getDelegation", params)

        for k, v in result.items():
            if isinstance(v, str) and v[:2] == "0x":
                result[k] = hex_to_int(v, 18)

        if len(result["delegations"]) > 0:
            delegations = result["delegations"]
            for delegation in delegations:
                delegation["value"] = hex_to_int(delegation["value"], 18)

        return result
