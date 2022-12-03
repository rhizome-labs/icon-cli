from icon_cli.icx import Icx
from icon_cli.tokens import Tokens
from icon_cli.utils import hex_to_int


class Omm(Icx):
    OMM_CONTRACT = "cx1a29259a59f463a67bb2ef84398b30ca56b5830a"
    OMM_ADDRESS_PROVIDER_CONTRACT = "cx6a66130200b4f08c65ef394469404378ab52e5b6"
    OMM_DAO_FUND_MANAGER_CONTRACT = "cx48a83a6fbdaa205a060514fd23ad6871c070f896"
    OMM_DELEGATION_CONTRACT = "cx841f29ec6ce98b527d49a275e87d427627f1afe5"
    OMM_FEE_PROVIDER_CONTACT = "cx4f3c2edf730f203b1ef1257d645415652ae8b4fb"
    OMM_GOVERNANCE_MANAGER_CONTRACT = "cx8190de91c8831f382dcabdbc87968448380c4838"
    OMM_LENDING_POOL_CONTRACT = "cxcb455f26a2c01c686fa7f30e1e3661642dd53c0d"
    OMM_LENDING_POOL_CORE_CONTRACT = "cxfb312bbd0a244b9e7bb5794c91f4e4acc41dea94"
    OMM_LENDING_POOL_DATA_PROVIDER_CONTRACT = (
        "cx5f9a6ca11b2b761a469965cedab40ada9e503cb5"
    )
    OMM_LIQUIDATION_MANAGER_CONTRACT = "cx533d76093a7b14fdbc3e213c7f987f1b6fea976c"
    OMM_PRICE_ORACLE_PROXY_CONTRACT = "cx189f03875da766878c68753da7492c080bcc2dbe"
    OMM_REWARD_DISTRIBUTION_CONTROLLER_CONTRACT = (
        "cx4f2d730ad969f5c839229de42184c5e47aefef6f"
    )
    OMM_STAKED_LP_CONTRACT = "cx015c7f8884d43519aa2bcf634140bd7328730cb6"

    def __init__(self, network) -> None:
        super().__init__(network)

    def update_delegation(self, wallet, prep_address):
        params = {
            "_delegations": [
                {"_address": prep_address, "_votes_in_per": 1000000000000000000}
            ]
        }
        transaction = self.build_call_transaction(
            wallet, self.OMM_DELEGATION_CONTRACT, 0, "updateDelegations", params
        )
        transaction_result = self.send_transaction(wallet, transaction)
        return transaction_result

    def get_omm_stake(self, icx_address):
        params = {"_owner": icx_address}
        result = self.call(Tokens().get_contract("OMM"), "staked_balanceOf", params)
        omm_stake = hex_to_int(result)
        return omm_stake
