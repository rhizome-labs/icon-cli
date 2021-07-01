import typer
from concurrent.futures import ThreadPoolExecutor
from icon_cli.models.Icx import Icx
from icon_cli.utils import hex_to_int


class Balanced(Icx):

    BALANCED_DAO_FUND_CONTRACT = "cx835b300dcfe01f0bdb794e134a0c5628384f4367"
    BALANCED_DEX_CONTRACT = "cxa0af3165c08318e988cb30993b3048335b94af6c"
    BALANCED_DIVIDENDS_CONTRACT = "cx13f08df7106ae462c8358066e6d47bb68d995b6d"
    BALANCED_GOVERNANCE_CONTRACT = "cx44250a12074799e26fdeee75648ae47e2cc84219"
    BALANCED_LOANS_CONTRACT = "cx66d4d90f5f113eba575bf793570135f9b10cece1"
    BALANCED_RESERVE_FUND_CONTRACT = "cxf58b9a1898998a31be7f1d99276204a3333ac9b3"
    BALANCED_REWARDS_CONTRACT = "cx10d59e8103ab44635190bd4139dbfd682fa2d07e"

    BALANCE_TOKEN_CONTRACT = "cxf61cd5a45dc9f91c15aa65831a30a90d59a09619"
    BALANCED_DOLLAR_CONTRACT = "cx88fd7df7ddff82f7cc735c871dc519838cb235bb"
    SICX_CONTRACT = "cx2609b924e33ef00b648a409245c7ea394c467824"

    LIQUIDATION_RATIO = 1500000000000000000

    def __init__(self, network) -> None:
        super().__init__(network)

    def liquidate_position(self, wallet, address: str):
        position = self.query_position_from_address(address)
        position_ratio = int(position["ratio"], 16)

        if position_ratio > 0 and position_ratio < self.LIQUIDATION_RATIO:
            transaction = self.build_call_transaction(
                wallet, self.BALANCED_LOANS_CONTRACT, "liquidate", {"_owner": address}
            )
            transaction_result = self.send_transaction(transaction)
            if len(transaction_result["eventLogs"]) > 0:
                return transaction_result
            else:
                print("Sorry, this position has already been liquidated.")
                raise typer.Exit()
        else:
            print(f"Sorry, {address} does not have a position that can be liquidated.")
            raise typer.Exit()

    def query_position_address(self, index: int) -> str:
        result = self.call(self.BALANCED_LOANS_CONTRACT, "getPositionAddress", {"_index": index})
        return result

    def query_position_count(self) -> int:
        result = self.call(self.BALANCED_LOANS_CONTRACT, "borrowerCount")
        position_count = int(result, 16)
        return position_count

    def query_position_from_address(self, address):
        params = {"_owner": address}
        result = self.call(self.BALANCED_LOANS_CONTRACT, "getAccountPositions", params)
        if "pos_id" not in result:
            print(f"{address} does not have a position on Balanced", 3)
            raise typer.Exit()
        else:
            position = self._format_position(result)
            return position

    def query_position_from_index(self, index: int) -> dict:
        address = self.query_position_address(index)
        position = self.query_position_from_address(address)
        return position

    def query_positions(
        self,
        index_start: int,
        index_end: int,
        min_collateralization: int,
        max_collateralization: int,
        sort_key: str,
        reverse: bool,
    ) -> list:
        positions = self._query_positions(index_start, index_end)

        filtered_positions = [
            position
            for position in positions
            if position["ratio"] * 100 >= min_collateralization
            and position["ratio"] * 100 <= max_collateralization  # noqa 503
        ]

        return sorted(filtered_positions, key=lambda i: i[sort_key], reverse=reverse)  # noqa 503

    @staticmethod
    def _format_position(position: dict) -> dict:
        for k, v in position.items():
            if isinstance(v, str) and v[:2] == "0x" and len(v) != 42:
                if k in ["collateral", "ratio", "total_debt"]:
                    value = hex_to_int(v)
                    if value != 0:
                        position[k] = hex_to_int(v) / 10 ** 18
                    else:
                        position[k] = hex_to_int(v)
                else:
                    position[k] = hex_to_int(v)
            if isinstance(v, dict) and k == "assets" and len(position["assets"]) > 0:
                for asset, amount in position["assets"].items():
                    value = hex_to_int(amount)
                    if value != 0:
                        position["assets"][asset] = hex_to_int(amount) / 10 ** 18
                    else:
                        position["assets"][asset] = hex_to_int(amount)
        return position

    ##############################
    # INTERNAL UTILITY FUNCTIONS #
    ##############################

    def _query_positions(self, index_start: int, index_end: int):
        with ThreadPoolExecutor() as executor:
            results = executor.map(self.query_position_from_index, range(index_start, index_end))
        return results
