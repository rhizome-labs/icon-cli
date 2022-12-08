from pathlib import PosixPath
from typing import Dict, List

from pydantic import BaseModel, validator
from yarl import URL

from icon_cli.utils import Utils


class IcxNetwork(BaseModel):
    name: str
    api_endpoint: URL
    nid: int
    tracker_endpoint: URL

    @validator("name")
    def validate_name(cls, name):
        name = Utils.strip_all_whitespace(name, force_lowercase=True)
        return name


class IcxKeystore(BaseModel):
    name: str
    file_path: PosixPath

    @validator("name")
    def validate_name(cls, name: str) -> str:
        name = Utils.strip_all_whitespace(name, force_lowercase=True)
        return name


class SavedIcxAddress(BaseModel):
    address: str

    @validator("address")
    def validate_address(cls, address: str) -> str:
        address = Utils.validate_address(address)
        return address


class AppConfig(BaseModel):
    custom_networks: Dict[IcxNetwork] = {}
    default_keystore: str = None
    default_network: str = "mainnet"
    keystores: Dict[IcxKeystore] = {}
    query_only: bool = False
    saved_addresses: Dict[SavedIcxAddress] = {}

    @validator("default_network")
    def validate_network_name(cls, name: str):
        name = Utils.strip_all_whitespace(name, force_lowercase=True)
        return name
