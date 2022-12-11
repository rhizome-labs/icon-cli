from icon_cli.httpreq import HttpReq


class Tracker:
    def __init__(self, network) -> None:
        self.icon_tracker_endpoint = "https://tracker.icon.community"

    def get_address_details(self, address: str):
        url = f"{self.icon_tracker_endpoint}/api/v1/addresses/details/{ address }/"
        address_details = HttpReq.get(url)
        return address_details

    def get_address_transactions(
        self,
        address: str,
        limit: int = 25,
        skip: int = 0,
    ):
        url = f"{self.icon_tracker_endpoint}/api/v1/transactions/address/{ address }/?limit={limit}&skip={skip}"
        transactions = HttpReq.get(url)
        return transactions
