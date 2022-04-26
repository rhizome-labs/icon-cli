import typer
from icon_cli.config import Config
from icon_cli.icx import Icx
from icon_cli.tokens import Tokens
from icon_cli.utils import format
from icon_cli.validators import Validators
from rich import inspect, print

app = typer.Typer()


@app.command()
def debug():
    inspect(__name__)


@app.command()
def balance(
    address: str = typer.Argument(..., callback=Validators.validate_address),
    network: str = typer.Option(
        Config.get_default_network(),
        "--network",
        "-n",
        callback=Validators.validate_network,
    ),
):
    balance = Icx(network).get_balance(address)
    print(f"{format(balance, 18)} ICX")


@app.command()
def token_balance(
    address: str = typer.Argument(..., callback=Validators.validate_address),
    network: str = typer.Option(
        Config.get_default_network(),
        "--network",
        "-n",
        callback=Validators.validate_network,
    ),
    contract: str = typer.Option(
        None, "--contract", "-c", callback=Validators.validate_contract
    ),
    ticker: str = typer.Option(
        None, "--ticker", "-t", callback=Validators.validate_token_ticker
    ),
):
    if ticker is not None:
        contract = Tokens.get_contract_from_ticker(ticker, network)
    balance = Icx(network).get_token_balance(address, contract)
    token_precision = Tokens.get_token_precision_from_contract(contract)
    print(f"{format(balance, token_precision)} {ticker}")
