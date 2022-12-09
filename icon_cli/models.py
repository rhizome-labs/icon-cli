from pathlib import Path
from typing import Dict, List

from pydantic import BaseModel, validator


class IcxNetwork(BaseModel):
    name: str
    api_endpoint: str
    nid: int
    tracker_endpoint: str

    @validator("name")
    def validate_name(cls, name):
        name = name.casefold()
        if name not in ["mainnet", "lisbon", "berlin", "sejong"]:
            raise ValueError(f"{name} is not a supported network name.")
        return name


class AppConfig(BaseModel):
    custom_networks: Dict[str, IcxNetwork] = {}
    default_keystore: str = None
    default_network: str = "mainnet"
    mode: str = "rw"
    saved_addresses: Dict[str, str] = {}

    @validator("mode")
    def validate_mode(cls, mode: str) -> str:
        if mode in ["r", "rw"]:
            return mode
