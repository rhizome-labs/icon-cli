from json import JSONDecodeError

import requests
from requests.exceptions import HTTPError

from icon_cli.utils import Utils


class HttpReq:
    def __init__(self) -> None:
        pass

    @staticmethod
    def get(url):
        try:
            r = requests.get(url)
            r.raise_for_status()
            if r.status_code == 200:
                data = r.json()
                return data
        except HTTPError:
            Utils.exit(f"Could not decode JSON response for request to {url}...", "error")  # fmt: skip
        except JSONDecodeError:
            Utils.exit(f"Could not decode JSON response for request to {url}...", "error")  # fmt: skip
