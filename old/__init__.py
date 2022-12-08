import builtins

import rich

from icon_cli.config import Config

Config.initialize_config()
builtins.print = rich.print
