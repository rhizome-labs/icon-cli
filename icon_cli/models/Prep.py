import requests
import typer
from icon_cli.models.Icx import Icx
from rich import print


class Prep(Icx):

    GOVERNANCE_CONTRACT = "cx0000000000000000000000000000000000000000"

    PREP_ADDRESSES_TO_NAMES = {
        "hxfba37e91ccc13ec1dab115811f73e429cde44d48": "ICX_Station",
        "hx9121c5914ce34f59de52fe15efd6f7982c2ab8ae": "ICON Asset Management",
        "hx3d5c3ce7554f4d762f6396e53b2c5de07074ec39": "ICON DAO",
        "hx231a795d1c719b9edf35c46b9daa4e0b5a1e83aa": "iBriz - ICONOsphere",
        "hx9780bfcd8d33c50f56e37f5b27313433c28eb8d8": "Stakin",
        "hxff6437443e7ed76d2d7f97f0d28d7ae1071bd0bb": "Spartan Node",
        "hx262afdeda4eba10fe41fa5ef21796ac2bdcc6629": "ICONation",
        "hxd0d9b0fee857de26fd1e8b15209ca15b14b851b2": "VELIC",
        "hx54d6f19c3d16b2ef23c09c885ca1ba776aaa80e2": "Ubik Capital",
        "hx4a43790d44b07909d20fbcc233548fc80f7a4067": "RHIZOME",
        "hxf08bd5835fdb53dc7c764a5f4dd4e2e6359324e8": "Metanyx",
        "hx8e6dcffdf06f850af5d372ac96389135e17d56d3": "Everstake",
        "hx0a72c03881451a6270d4895f756085470fc311e4": "ICON Pinas",
        "hxb11448743cbb63fcf29609401cdc5782793be211": "ICONbet Community",
        "hx6f89b2c25c15f6294c79810221753131067ed3f8": "Staky.io (ex Sharpn)",
        "hxdc35f82a3a943e040ae2b9ab2baa2118781b2bc9": "Mineable",
        "hxd6f20327d135cb0227230ab98792173a5c97b03e": "ICONPLUS",
        "hx1cb5883939f2fd478e92da1260438aa1f03440ca": "ICON Sweden",
        "hxc97bc2b6863b5f0094de7f0e5bcf82a404c4199b": "Silicon Valley ICON",
        "hxc5e0b88cb9092bbd8b004a517996139334752f62": "Foundry Box Media",
        "hxca60d4371ad90d624dc7119f81009d799c168aa1": "devshack",
        "hxf0e7b39f0d43591c9a5c823eb19b90462fa51c30": "ICON France",
        "hx6fefe6d0174357ba1c8f086a54ab1b277064e65f": "TEMPO",
        "hx55f2cc3244350085734f4e405f761ecf3d2095b3": "Staked Tech",
        "hx9fa9d224306b0722099d30471b3c2306421aead7": "Espanicon",
        "hx5dff0f5953e8cb0d50aaabff041a524e27718bd2": "DSNC",
        "hx135d9c1b6ad2b7750f153d1649b676f8625e470c": "ICON Guide Star",
        "hx2f3fb9a9ff98df2145936d2bfcaa3837a289496b": "Transcranial Solutions",
        "hxfa6714e4ec784ae2176c416c46dc2c98b6ec9074": "PiconbelloDAO",
        "hxa615b432cb84c3f2ed22194b32df317b474ec2c9": "HOLA ICON",
        "hxe0df49d9382805d4dfa24487e8ef31165fe782c0": "loop57",
        "hxfc56203484921c3b7a4dee9579d8614d8c8daaf5": "Geometry Labs",
    }

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

    @classmethod
    def convert_address_to_name(cls, address):
        if address in cls.PREP_ADDRESSES_TO_NAMES.keys():
            return cls.PREP_ADDRESSES_TO_NAMES[address]
        else:
            print(f"Sorry, {address} is not a valid P-Rep address.")
            raise typer.Exit()

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
