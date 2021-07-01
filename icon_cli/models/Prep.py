import requests
import typer
from icon_cli.models.Icx import Icx
from rich import print


class Prep(Icx):

    GOVERNANCE_CONTRACT = "cx0000000000000000000000000000000000000000"

    def __init__(self, network) -> None:
        super().__init__(network)

    def query_prep_by_name(self, name):
        preps = self.call(self.GOVERNANCE_CONTRACT, "getPReps", None)["preps"]
        prep_map = {}
        for prep in preps:
            prep_map[prep["name"]] = prep
        for key, value in prep_map.items():
            if name.lower() in key.lower():
                return value
            else:
                print(f"Oops, there are no P-Reps named {name}.")
                raise typer.Exit()

    def query_prep_by_address(self, address):
        prep = self.call(self.GOVERNANCE_CONTRACT, "getPRep", {"address": address})
        return prep

    def query_preps(self, range_start, range_end):
        preps = self.call(
            self.GOVERNANCE_CONTRACT,
            "getPReps",
            {"startRanking": range_start, "endRanking": range_end},
        )["preps"]
        return preps

    ##############################
    # EXTERNAL UTILITY FUNCTIONS #
    ##############################

    @staticmethod
    def query_prep_count():
        try:
            r = requests.get("https://tracker.icon.foundation/v3/iiss/prep/list?count=500", timeout=0.5)
            r.raise_for_status()
            prep_count = r.json()["totalSize"]
        except Exception:
            prep_count = 100
        return prep_count

    ##############################
    # INTERNAL UTILITY FUNCTIONS #
    ##############################

    @staticmethod
    def _strip_prep_name_bs(name):
        prep_name_bs = {
            "iconleo": "ICONLEO",
            "icxburners": "ICXburners",
            "unblock": "UNBLOCK",
            "gilga": "Gilga Capital",
            "iconist vote wisely": "ICONIST VOTE WISELY",
        }
        for key, value in prep_name_bs.items():
            if key in name.lower():
                return value
            else:
                return name

    @staticmethod
    def _format_prep_json_response(prep: dict):
        pass
