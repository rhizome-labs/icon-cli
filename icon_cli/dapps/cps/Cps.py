from icon_cli.icx import Icx
from icon_cli.utils import hex_to_int


class Cps(Icx):
    def __init__(self, network) -> None:
        super().__init__(network)
        self.CPS_CONTRACT = "cx9f4ab72f854d3ccdc59aa6f2c3e2215dd62e879f"

    def query_active_proposals(self, address):
        proposals = self.call(
            self.CPS_CONTRACT,
            "get_active_proposals",
            {"_wallet_address": address},
        )
        if len(proposals) > 0:
            for proposal in proposals:
                proposal["new_progress_report"] = hex_to_int(proposal["new_progress_report"])  # noqa 503
                proposal["last_progress_report"] = hex_to_int(proposal["last_progress_report"])  # noqa 503
        return address, proposals

    def query_cps_balance(self):
        balance = self.call(self.CPS_CONTRACT, "get_remaining_fund", None)
        return hex_to_int(balance) / 10 ** 18

    def query_cps_contributors(self) -> list:
        params = {"_start_index": 0, "_end_index": 100}
        contributors = self.call(self.CPS_CONTRACT, "get_contributors", params)
        return contributors

    def query_cps_preps(self):
        preps = self.call(self.CPS_CONTRACT, "get_PReps", None)
        for prep in preps:
            prep["delegated"] = hex_to_int(prep["delegated"]) / 10 ** 18
        return preps

    def query_period_status(self):
        period_status = self.call(self.CPS_CONTRACT, "get_period_status", None)
        for k, v in period_status.items():
            if k in [
                "current_block",
                "next_block",
                "remaining_time",
                "period_span",
            ]:  # noqa 503
                period_status[k] = hex_to_int(v)
        return period_status

    def query_proposal_details(self, address):
        params = {"_wallet_address": address}
        proposal_details = self.call(self.CPS_CONTRACT, "get_proposal_detail_by_wallet", params)
        proposals = proposal_details["data"]
        for proposal in proposals:
            for k, v in proposal.items():
                if v[:2] == "0x" and len(v) != 42:
                    proposal[k] = hex_to_int(v)
        return proposals

    def query_project_amounts(self):
        result = self.call(self.CPS_CONTRACT, "get_project_amounts", None)
        print(result)