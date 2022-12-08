from pathlib import PosixPath
from typing import Dict, List

from pydantic import BaseModel, validator

from icon_cli.utils import Utils


class IcxNetwork(BaseModel):
    name: str
    api_endpoint: str
    nid: int
    tracker_endpoint: str

    @validator("name")
    def validate_name(cls, name: str):
        name = Utils.strip_all_whitespace(name, force_lowercase=True)
        return name

    @validator("api_endpoint")
    def validate_api_endpoint(cls, api_endpoint: str):
        url = Utils.validate_url(api_endpoint)
        return url

    @validator("tracker_endpoint")
    def validate_tracker_endpoint(cls, tracker_endpoint: str):
        url = Utils.validate_url(tracker_endpoint)
        return url


class SavedIcxAddress(BaseModel):
    address: str

    @validator("address")
    def validate_address(cls, address: str) -> str:
        address = Utils.validate_address(address)
        return address


class AppConfig(BaseModel):
    custom_networks: Dict[str, IcxNetwork] = {}
    default_keystore: str = None
    default_network: str = "mainnet"
    keystores: List[str] = []
    mode: str = "rw"
    saved_addresses: Dict[str, SavedIcxAddress] = {}

    @validator("default_network")
    def validate_network_name(cls, name: str) -> str:
        name = Utils.strip_all_whitespace(name, force_lowercase=True)
        return name

    @validator("mode")
    def validate_mode(cls, mode: str) -> str:
        if mode in ["r", "rw"]:
            return mode
