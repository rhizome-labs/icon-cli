from pathlib import Path

import typer
from icon_cli.config import Config
from icon_cli.validators import Validators

app = typer.Typer()


@app.command()
def add(
    address: str = typer.Argument(..., callback=Validators.validate_address),
    name: str = typer.Argument(..., callback=Validators.validate_lowercase_only),
):
    """
    Add an ICX address to the address book.
    """
    Config.add_address_to_address_book(address, name)


@app.command()
def delete(
    name: str = typer.Argument(
        ..., callback=Validators.validate_address_book_address_name
    )
):
    """
    Delete an ICX address from the address book.
    """
    Config.delete_address_from_address_book(name)
