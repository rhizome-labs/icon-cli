from typing import Dict

from pydantic import BaseModel, validator


class IcxNetwork(BaseModel):
    name: str
    api_endpoint: str
    nid: int
    tracker_endpoint: str

    class Config:
        anystr_strip_whitespace = True
        anystr_lower = True

    @validator("name")
    def validate_name(cls, name):
        if name not in ["mainnet", "lisbon", "berlin", "sejong"]:
            raise ValueError(f"{name} is not a supported network name.")
        return name


class IcxToken(BaseModel):
    symbol: str
    decimals: int = None
    mainnet: str = None
    testnet: str = None


class AppConfig(BaseModel):
    custom_networks: Dict[str, IcxNetwork] = {}
    default_keystore: str = None
    default_network: str = "mainnet"
    mode: str = "rw"
    saved_addresses: Dict[str, str] = {}

    class Config:
        anystr_strip_whitespace = True
        anystr_lower = True

    @validator("mode")
    def validate_mode(cls, mode: str) -> str:
        if mode in ["r", "rw"]:
            return mode

    @validator("default_network")
    def validate_default_network(cls, name):
        if name not in ["mainnet", "lisbon", "berlin", "sejong"]:
            raise ValueError(f"{name} is not a supported network name.")
        return name
