class Tokens:

    TOKENS = {
        "BALN": {
            "ticker": "BALN",
            "precision": 18,
            "contracts": {
                "mainnet": "cxf61cd5a45dc9f91c15aa65831a30a90d59a09619",
            },
        },
        "OMM": {
            "ticker": "OMM",
            "precision": 18,
            "contracts": {
                "mainnet": "cx1a29259a59f463a67bb2ef84398b30ca56b5830a",
            },
        },
    }

    PRECISION = {
        "mainnet": {
            "cx1a29259a59f463a67bb2ef84398b30ca56b5830a": 18,
            "cxf61cd5a45dc9f91c15aa65831a30a90d59a09619": 18,
        }
    }

    def __init__(self) -> None:
        pass

    @classmethod
    def get_contract_from_ticker(cls, ticker: str, network: str) -> str:
        contract = cls.TOKENS[ticker]["contracts"][network]
        return contract

    @classmethod
    def get_token_precision_from_contract(cls, contract: str, network: str) -> int:
        precision = cls.PRECISION[network][contract]
        return precision
