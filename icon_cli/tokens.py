from icon_cli.models import IcxToken


class Tokens:

    TOKENS = {
        "baln": IcxToken(
            symbol="BALN",
            decimals=18,
            mainnet="cxf61cd5a45dc9f91c15aa65831a30a90d59a09619",
        )
    }

    def __init__(self) -> None:
        pass

    @classmethod
    def get_token(cls, symbol: str):
        return cls.TOKENS[symbol.casefold()]

    @classmethod
    def get_token_contract(cls, symbol: str, network: str):
        return cls.TOKENS[symbol.casefold()][network]
