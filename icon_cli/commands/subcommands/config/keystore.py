import typer
from icon_cli.models.Config import Config
from pathlib import Path

app = typer.Typer()


@app.command()
def debug():
    print(__name__)


@app.command()
def add(
    keystore_path: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        writable=False,
        resolve_path=True,
    )
):
    """
    Import an ICX keystore to use in icon-cli.
    """
    config = Config()
    config.import_keystore(keystore_path)
