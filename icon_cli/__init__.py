import logging
import os
from dotenv import load_dotenv
from rich.logging import RichHandler

__version__ = "0.1.0"

# Load environment variables.
load_dotenv()

# Configure debug logger.
if os.environ["ENV"] == "DEV":
    log_level = "DEBUG"
else:
    log_level = "ERROR"

logging.basicConfig(level=log_level, format="%(message)s", datefmt="[%X]", handlers=[RichHandler()])
log = logging.getLogger("rich")
