from icon_cli.models import IcxContract


class Contracts:

    KNOWN_CONTRACTS = {
        "chain": IcxContract(
            name="Chain",
            mainnet="cx0000000000000000000000000000000000000000",
            lisbon="cx0000000000000000000000000000000000000000",
            berlin="cx0000000000000000000000000000000000000000",
            sejong="cx0000000000000000000000000000000000000000",
            localhost="cx0000000000000000000000000000000000000000",
        ),
        "governance": IcxContract(
            name="Governance",
            mainnet="cx0000000000000000000000000000000000000001",
            lisbon="cx0000000000000000000000000000000000000001",
            berlin="cx0000000000000000000000000000000000000001",
            sejong="cx0000000000000000000000000000000000000001",
            localhost="cx0000000000000000000000000000000000000001",
        ),
        "balancedDex": IcxContract(
            name="Balanced DEX",
            mainnet="cxa0af3165c08318e988cb30993b3048335b94af6c",
        ),
    }

    def __init__(self) -> None:
        pass

    @classmethod
    def get_contract_from_name(cls, name: str):
        return cls.KNOWN_CONTRACTS[name]

    @classmethod
    def get_known_contract_names(cls):
        return cls.KNOWN_CONTRACTS.keys()
