from pathlib import Path
from typing import Dict, List

from pydantic import BaseModel, validator


class IcxNetwork(BaseModel):
    name: str
    api_endpoint: str
    nid: int
    tracker_endpoint: str


class SavedIcxAddress(BaseModel):
    address: str


class AppConfig(BaseModel):
    custom_networks: Dict[str, IcxNetwork] = {}
    default_keystore: str = None
    default_network: str = "mainnet"
    mode: str = "rw"
    saved_addresses: Dict[str, SavedIcxAddress] = {}

    @validator("mode")
    def validate_mode(cls, mode: str) -> str:
        if mode in ["r", "rw"]:
            return mode
