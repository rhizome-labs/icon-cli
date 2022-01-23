class Tokens:

    TOKENS = {
        "BALN": {
            "ticker": "BALN",
            "contract": "cxf61cd5a45dc9f91c15aa65831a30a90d59a09619",
            "exa": 18
        },
        "SICX": {
            "ticker": "sICX",
            "contract": "cx2609b924e33ef00b648a409245c7ea394c467824",
            "exa": 18
        }
    }

    def token_name_to_contract(self, token_name):
        contract = self.TOKENS[token_name.upper()]["contract"]
        return contract
