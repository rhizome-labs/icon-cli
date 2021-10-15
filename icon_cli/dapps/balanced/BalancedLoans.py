import typer
from concurrent.futures import ThreadPoolExecutor
from icon_cli.dapps.balanced.Balanced import Balanced
from icon_cli.utils import hex_to_int


class BalancedLoans(Balanced):

    LIQUIDATION_RATIO = 1.5

    def __init__(self, network) -> None:
        super().__init__(network)

    ##################
    # CALL FUNCTIONS #
    ##################

    def query_position_address(self, index: int) -> str:
        """
        Query the position address for a given position index.

        Args:
            index: Index of the Balanced position to query.

        Returns:
            The ICX address of the queried position.
        """
        result = self.call(self.BALANCED_LOANS_CONTRACT,
                           "getPositionAddress", {"_index": index})
        return result

    def query_position_count(self) -> int:
        result = self.call(self.BALANCED_LOANS_CONTRACT, "borrowerCount")
        position_count = int(result, 16)
        return position_count

    def query_position_from_address(self, address):
        params = {"_owner": address}
        result = self.call(self.BALANCED_LOANS_CONTRACT,
                           "getAccountPositions", params)
        if "pos_id" not in result:
            print(f"{address} does not have a position on Balanced")
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

    def query_rebalance_status(self):
        rebalance_status = self.call(
            self.BALANCED_REBALANCE_CONTRACT, "getRebalancingStatus", {})
        return rebalance_status

    #########################
    # TRANSACTION FUNCTIONS #
    #########################

    def borrow_bnusd(self, wallet, borrow_amount):
        params = {"_asset": "bnUSD", "_amount": borrow_amount}
        transaction = self.build_call_transaction(
            wallet, self.BALANCED_LOANS_CONTRACT, 0, "depositAndBorrow", params
        )
        transaction_result = self.send_transaction(wallet, transaction)
        return transaction_result

    def deposit_icx(self, wallet, icx_deposit_amount: int = 0):
        params = {"_asset": "bnUSD", "_amount": 0}
        transaction = self.build_call_transaction(
            wallet, self.BALANCED_LOANS_CONTRACT, icx_deposit_amount, "depositAndBorrow", params
        )
        transaction_result = self.send_transaction(wallet, transaction)
        return transaction_result

    def deposit_sicx(self, wallet, sicx_deposit_amount: int):
        params = {
            "_to": self.BALANCED_LOANS_CONTRACT,
            "_value": sicx_deposit_amount,
            "_data": "0x7b225f6173736574223a22222c225f616d6f756e74223a307d",
        }
        transaction = self.build_call_transaction(
            wallet, self.SICX_CONTRACT, 0, "transfer", params)
        transaction_result = self.send_transaction(wallet, transaction)
        return transaction_result

    def liquidate(self, wallet, address: str) -> dict:
        """Liquidates a bad position on Balanced. #REKT

        Args:
            wallet: An ICX KeyWallet object.
            address: The ICX address of the position owner to liquidate.

        Returns:
            A dictionary containing transaction metadata.
        """
        position = self.query_position_from_address(address)
        position_ratio = position["ratio"]

        if position_ratio > 0 and position_ratio < self.LIQUIDATION_RATIO:
            transaction = self.build_call_transaction(
                wallet, self.BALANCED_LOANS_CONTRACT, "liquidate", {
                    "_owner": address}
            )
            transaction_result = self.send_transaction(transaction)
            if len(transaction_result["eventLogs"]) > 0:
                return transaction_result
            else:
                print("Sorry, this position has already been liquidated.")
                raise typer.Exit()
        else:
            print(
                f"Sorry, {address} does not have a position that can be liquidated.")
            raise typer.Exit()

    def rebalance(self, wallet, verify_transaction=True):
        rebalance_status = self.call(
            self.BALANCED_REBALANCE_CONTRACT, "getRebalancingStatus", {})
        if rebalance_status[0] == "0x1" or rebalance_status[2] == "0x1":
            transaction = self.build_call_transaction(
                wallet, self.BALANCED_REBALANCE_CONTRACT, 0, "rebalance", {}
            )
            transaction_result = self.send_transaction(
                wallet, transaction, verify_transaction=verify_transaction)
            return transaction_result
        else:
            print("There are no positions to rebalance right now.")
            exit()

    def withdraw_collateral(self, wallet, amount: int):
        params = {"_value": amount}
        transaction = self.build_call_transaction(
            wallet, self.BALANCED_LOANS_CONTRACT, 0, "withdrawCollateral", params
        )
        transaction_result = self.send_transaction(wallet, transaction)
        return transaction_result

    ##############################
    # INTERNAL UTILITY FUNCTIONS #
    ##############################

    def _query_positions(self, index_start: int, index_end: int):
        with ThreadPoolExecutor() as executor:
            results = executor.map(
                self.query_position_from_index, range(index_start, index_end))
        return results

    @staticmethod
    def _format_position(position: dict) -> dict:
        for k, v in position.items():
            if isinstance(v, str) and v[:2] == "0x" and len(v) != 42:
                if k in ["collateral", "ratio", "total_debt"]:
                    value = hex_to_int(v)
                    if value != 0:
                        position[k] = hex_to_int(v)
                    else:
                        position[k] = hex_to_int(v)
                else:
                    position[k] = hex_to_int(v)
            if isinstance(v, dict) and k == "assets" and len(position["assets"]) > 0:
                for asset, amount in position["assets"].items():
                    value = hex_to_int(amount)
                    if value != 0:
                        position["assets"][asset] = hex_to_int(amount)
                    else:
                        position["assets"][asset] = hex_to_int(amount)
        return position
