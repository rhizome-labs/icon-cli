import typer
from icon_cli.models.Icx import Icx
from rich import print


class Preps(Icx):

    GOVERNANCE_CONTRACT = "cx0000000000000000000000000000000000000000"

    def __init__(self, network) -> None:
        super().__init__(network)

    @classmethod
    def query_prep_by_name(cls, name):
        preps = cls.call(cls.GOVERNANCE_CONTRACT, "getPReps", None)["preps"]
        prep_map = {}
        for prep in preps:
            prep_map[prep["name"]] = prep
        for key, value in prep_map.items():
            if name.lower() in key.lower():
                return value
            else:
                print(f"Oops, there are no P-Reps named {name}.")
                raise typer.Exit()

    @classmethod
    def query_prep_by_address(cls, address):
        prep = cls.call(cls.GOVERNANCE_CONTRACT, "getPRep", {"address": address})
        return prep

    @classmethod
    def query_preps(cls, range_start, range_end):
        preps = cls.call(
            cls.GOVERNANCE_CONTRACT,
            "getPReps",
            {"startRanking": range_start, "endRanking": range_end},
        )["preps"]
        return preps

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
