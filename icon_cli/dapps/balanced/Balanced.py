from enum import Enum
from icon_cli.models.Icx import Icx


class Balanced(Icx):

    BALANCED_DAO_FUND_CONTRACT = "cx835b300dcfe01f0bdb794e134a0c5628384f4367"
    BALANCED_DEX_CONTRACT = "cxa0af3165c08318e988cb30993b3048335b94af6c"
    BALANCED_DIVIDENDS_CONTRACT = "cx203d9cd2a669be67177e997b8948ce2c35caffae"
    BALANCED_GOVERNANCE_CONTRACT = "cx44250a12074799e26fdeee75648ae47e2cc84219"
    BALANCED_LOANS_CONTRACT = "cx66d4d90f5f113eba575bf793570135f9b10cece1"
    BALANCED_RESERVE_FUND_CONTRACT = "cxf58b9a1898998a31be7f1d99276204a3333ac9b3"
    BALANCED_REWARDS_CONTRACT = "cx10d59e8103ab44635190bd4139dbfd682fa2d07e"

    BALANCE_TOKEN_CONTRACT = "cxf61cd5a45dc9f91c15aa65831a30a90d59a09619"
    BALANCED_DOLLAR_CONTRACT = "cx88fd7df7ddff82f7cc735c871dc519838cb235bb"
    SICX_CONTRACT = "cx2609b924e33ef00b648a409245c7ea394c467824"

    GEOMETRY_API_ENDPOINT = "https://balanced.geometry.io/api/v1"

    def __init__(self, network) -> None:
        super().__init__(network)


class BalancedCollateralAsset(str, Enum):
    icx = "icx"
    sicx = "sicx"
