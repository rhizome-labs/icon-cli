from pathlib import Path

import typer
from icon_cli.config import Config
from icon_cli.validators import Validators

app = typer.Typer()


@app.command()
def import_keystore(
    keystore_path: Path = typer.Argument(
        ...,
        callback=Validators.validate_keystore,
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        writable=False,
        resolve_path=True,
    )
):
    """
    Import an ICX wallet keystore.
    """
    Config.import_keystore(keystore_path)
