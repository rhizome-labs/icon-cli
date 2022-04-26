class Contracts:

    CONTRACTS = {
        "balanced_dao_fund": {"mainnet": "cx835b300dcfe01f0bdb794e134a0c5628384f4367"},
        "balanced_dex": {"mainnet": "cxa0af3165c08318e988cb30993b3048335b94af6c"},
        "balanced_dividends": {"mainnet": "cx203d9cd2a669be67177e997b8948ce2c35caffae"},
        "balanced_governance": {
            "mainnet": "cx44250a12074799e26fdeee75648ae47e2cc84219"
        },
        "balanced_loans": {"mainnet": "cx66d4d90f5f113eba575bf793570135f9b10cece1"},
        "balanced_rebalance": {"mainnet": "cx40d59439571299bca40362db2a7d8cae5b0b30b0"},
        "balanced_reserve_fund": {
            "mainnet": "cxf58b9a1898998a31be7f1d99276204a3333ac9b3"
        },
        "cps": {"mainnet": "cx9f4ab72f854d3ccdc59aa6f2c3e2215dd62e879f"},
    }

    def __init__(self) -> None:
        pass

    @classmethod
    def get_contract_from_name(cls, name: str, network: str) -> str:
        contract = cls.CONTRACTS[name][network]
        return contract
