import typer
from icon_cli.config import Config
from icon_cli.icx import Icx
from icon_cli.validators import Validators


app = typer.Typer()


@app.command()
def abi(
    contract: str = typer.Argument(..., callback=Validators.validate_contract),
    network: str = typer.Option(
        Config.get_default_network(),
        "--network",
        "-n",
        callback=Validators.validate_network,
    ),
):
    abi = Icx(network).get_contract_abi(contract)
    print(abi)
