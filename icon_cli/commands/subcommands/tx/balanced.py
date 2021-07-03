import typer
from icon_cli.dapps.balanced.BalancedLoans import BalancedLoans
from icon_cli.dapps.balanced.BalancedDividends import BalancedDividends
from icon_cli.models.Callbacks import Callbacks
from icon_cli.models.Config import Config
from icon_cli.utils import print_object
from rich import print

app = typer.Typer()


@app.command()
def debug():
    print_object(__name__)


@app.command()
def distribute(
    keystore: str = typer.Option(
        Config.get_default_keystore(),
        "--keystore",
        "-k",
        callback=Callbacks.load_wallet_from_keystore,
    ),
    network: str = typer.Option(
        Config.get_default_network(), "--network", "-n", callback=Callbacks.enforce_mainnet
    ),
):
    balanced_dividends = BalancedDividends(network)
    distribution_check = balanced_dividends.distribution_check()

    if distribution_check == 0:
        balanced_dividends.distribute_dividends(keystore)
        print("Reward distribution has been triggered.")
    else:
        print("Reward distribution is already finished.")


@app.command()
def liquidate(
    address: str = typer.Argument(..., callback=Callbacks.validate_icx_address),
    wallet: str = typer.Option(
        Config.get_default_keystore(),
        "--keystore",
        "-k",
        callback=Callbacks.load_wallet_from_keystore,
    ),
    network: str = typer.Option(
        Config.get_default_network(),
        "--network",
        "-n",
        callback=Callbacks.enforce_mainnet,
    ),
):
    balanced_loans = BalancedLoans(network)
    transaction_result = balanced_loans.liquidate_position(wallet, address)

    print(f"{address} has been liquidated: {transaction_result['txHash']}")


@app.command()
def order(
    pool: str = typer.Argument(...),
):
    pass


@app.command()
def provide(
    pool: str = typer.Argument(...),
    amount: int = typer.Argument(...),
    network: str = typer.Option(
        Config.get_default_network(),
        "--network",
        "-n",
        callback=Callbacks.enforce_mainnet,
    ),
):
    pass


@app.command()
def retire_bnusd(
    amount: int = typer.Argument(...),
    network: str = typer.Option(
        Config.get_default_network(),
        "--network",
        "-n",
        callback=Callbacks.enforce_mainnet,
    ),
):
    pass


@app.command()
def swap(
    source_asset: str = typer.Argument(...),
    destination_asset: str = typer.Argument(...),
    network: str = typer.Option(
        Config.get_default_network(),
        "--network",
        "-n",
        callback=Callbacks.enforce_mainnet,
    ),
):
    pass
