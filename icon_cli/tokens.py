class Tokens:

    TOKENS = {
        "BALN": {
            "ticker": "BALN",
            "contract": "cxf61cd5a45dc9f91c15aa65831a30a90d59a09619",
            "exa": 18,
        },
        "OMM": {
            "ticker": "OMM",
            "contract": "cx1a29259a59f463a67bb2ef84398b30ca56b5830a",
            "exa": 18,
        },
        "SICX": {
            "ticker": "sICX",
            "contract": "cx2609b924e33ef00b648a409245c7ea394c467824",
            "exa": 18,
        },
    }

    def token_name_to_contract(self, token_name):
        contract = self.TOKENS[token_name.upper()]["contract"]
        return contract

    def get_contract(self, token_name: str) -> str:
        contract = self.TOKENS[token_name.upper()]["contract"]
        return contract
