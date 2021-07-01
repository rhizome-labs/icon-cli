import logging
import os
from dotenv import load_dotenv
from rich.logging import RichHandler


class Log:

    load_dotenv()

    if os.getenv("ENV") == "DEBUG":
        log_level = "DEBUG"
    else:
        log_level = "ERROR"

    logging.basicConfig(level=log_level, format="%(message)s", datefmt="[%X]", handlers=[RichHandler()])

    log = logging.getLogger("rich")
