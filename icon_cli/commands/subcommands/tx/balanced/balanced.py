import typer
from icon_cli.commands.subcommands.tx.balanced import balanced_pool
from icon_cli.dapps.balanced.Balanced import BalancedCollateralAsset
from icon_cli.dapps.balanced.BalancedLoans import BalancedLoans
from icon_cli.dapps.balanced.BalancedDividends import BalancedDividends
from icon_cli.models.Icx import IcxNetwork
from icon_cli.models.Callbacks import Callbacks
from icon_cli.models.Config import Config
from icon_cli.utils import (
    die,
    format_number_display,
    log,
    print_json,
    print_object,
    print_tx_hash,
    to_loop,
)
from rich import print

app = typer.Typer()

app.add_typer(balanced_pool.app, name="pool")


@app.command()
def debug():
    print_object(__name__)


@app.command()
def borrow(
    borrow_amount: float = typer.Argument(..., callback=Callbacks.validate_transaction_value),
    keystore: str = typer.Option(
        Config.get_default_keystore(),
        "--keystore",
        "-k",
        callback=Callbacks.load_wallet_from_keystore,
    ),
    network: IcxNetwork = typer.Option(
        Config.get_default_network(),
        "--network",
        "-n",
        callback=Callbacks.enforce_mainnet,
        case_sensitive=False,
    ),
    skip: bool = typer.Option(False, "--skip", "-s"),
    max: bool = typer.Option(False, "--max", "-max"),
    threshold: bool = typer.Option(False, "--threshold", "-t"),
):
    # Raise exception if both --max and --threshold are specified.
    if max is True and threshold is True:
        die("Sorry, you can't use --max and --threshold at the same time. Please choose one.")

    # Raise exception if loan size is less than 10 bnUSD.
    if borrow_amount < 10:
        die("Sorry, the minimum loan size is 10 bnUSD.")

    balanced_loans = BalancedLoans(network)

    # Fetch ICX price and Balanced position details to calculate max loan size.
    icx_price = balanced_loans.query_icx_usd_price()
    balanced_position = balanced_loans.query_position_from_address(keystore.get_address())
    collateral = balanced_position["assets"]["sICX"]
    collateral_value = collateral * icx_price
    max_borrow_amount = collateral_value * 0.25
    threshold_borrow_amount = collateral_value * 0.2

    log(
        f"Collateral: {collateral}\n"
        f"Collateral Value: {collateral_value}\n"
        f"Max Borrow: {max_borrow_amount}\n"
        f"Threshold Borrow: {threshold_borrow_amount}"
    )

    # Override borrow_amount if --max or --threshold is True.
    if max is True:
        borrow_amount = max_borrow_amount
    if threshold is True:
        borrow_amount = threshold_borrow_amount

    # Raise exception if borrow_amount is greater than max_borrow_amount.
    if borrow_amount > max_borrow_amount:
        print(
            f"Sorry, you don't have enough collateral to borrow {format_number_display(borrow_amount, 0, 8)} bnUSD.\n"
            f"Your maximum loan size is {format_number_display(max_borrow_amount, 0, 8)} bnUSD."
        )
        die()

    # Ask use to confirm borrow
    if skip is False:
        if borrow_amount >= threshold_borrow_amount and borrow_amount < max_borrow_amount:
            borrow_confirmation = typer.confirm(
                f"To earn BALN rewards, your loan size needs to be less than {format_number_display(threshold_borrow_amount, 0, 2)} bnUSD.\n"  # noqa 503
                f"Would you like to proceed with borrowing {format_number_display(borrow_amount, 0, 2)} bnUSD?"
            )
        else:
            borrow_confirmation = typer.confirm(
                f"Please confirm you'd like to take a {format_number_display(borrow_amount, 0, 2)} bnUSD loan."
            )
        if not borrow_confirmation:
            die()

    transaction_result = balanced_loans.deposit_and_borrow(keystore, 0, to_loop(borrow_amount))

    print_tx_hash(transaction_result)


@app.command()
def deposit(
    asset: BalancedCollateralAsset = typer.Argument(..., case_sensitive=False),
    amount: str = typer.Argument(0, callback=Callbacks.validate_transaction_value),
    keystore: str = typer.Option(
        Config.get_default_keystore(),
        "--keystore",
        "-k",
        callback=Callbacks.load_wallet_from_keystore,
    ),
    network: IcxNetwork = typer.Option(
        Config.get_default_network(),
        "--network",
        "-n",
        callback=Callbacks.enforce_mainnet,
        case_sensitive=False,
    ),
    max: bool = typer.Option(False, "--max", "-m"),
    skip: bool = typer.Option(False, "--skip", "-s"),
):
    balanced_loans = BalancedLoans(network)

    if asset == "icx":
        icx_balance = balanced_loans.query_icx_balance(keystore.get_address())
        minimum_balance = 2 * balanced_loans.EXA
        max_icx_deposit_amount = int(icx_balance - minimum_balance)

        # Set deposit amount to max_deposit_amount if --max is used.
        if max is True:
            amount = max_icx_deposit_amount

        # Exit if balance is less than 2 ICX, or if amount is less than 0.
        if icx_balance < minimum_balance or amount < 0:
            die(
                "Sorry, you need a minimum balance of 2 ICX to deposit collateral into Balanced.\n"
                f"Your current balance is {format_number_display(icx_balance, 18, 18)} ICX."
            )

        log(
            f"{icx_balance} {icx_balance / 10 ** 18} (ICX Balance)\n"
            f"{max_icx_deposit_amount} {max_icx_deposit_amount / 10 ** 18} (Max ICX Deposit)\n"
            f"{amount} (Deposit Amount)"
        )

        # Exit if ICX balance is less than deposit amount.
        if icx_balance < amount:
            die(
                f"Sorry, you can't deposit {format_number_display(amount, 18, 18)} ICX.\n"
                f"Your maximum deposit amount is {format_number_display(max_icx_deposit_amount, 18, 18)} ICX"
            )

        if skip is False:
            confirmation_prompt = typer.confirm(
                f"Please confirm you'd like to deposit {format_number_display(amount, 18, 18)} ICX."
            )
            if not confirmation_prompt:
                die()

        print(f"Depositing {format_number_display(amount, 18, 18)} ICX now...")
        transaction_result = balanced_loans.deposit_icx(keystore, amount)

    if asset == "sicx":
        sicx_balance = balanced_loans.query_token_balance(keystore.get_address(), "SICX")

        if sicx_balance <= 0:
            die("Sorry, you don't have any sICX to deposit.")

        if max is True:
            amount = sicx_balance

        log(f"sICX Balance {sicx_balance}\n" f"Deposit Amount: {amount}")

        if sicx_balance < amount:
            print(
                f"Sorry, you can't deposit {format_number_display(amount, 18, 18)} sICX.\n"
                f"Your maximum deposit amount is {format_number_display(sicx_balance, 18, 18)} sICX"
            )

        if skip is False:
            confirmation_prompt = typer.confirm(
                f"Please confirm you'd like to deposit {format_number_display(amount, 18, 18)} sICX."
            )
            if not confirmation_prompt:
                die()

        print(f"Depositing {amount} sICX now...")
        transaction_result = balanced_loans.deposit_sicx(keystore, amount)

    print_tx_hash(transaction_result)


@app.command()
def distribute(
    keystore: str = typer.Option(
        Config.get_default_keystore(),
        "--keystore",
        "-k",
        callback=Callbacks.load_wallet_from_keystore,
    ),
    network: IcxNetwork = typer.Option(
        Config.get_default_network(),
        "--network",
        "-n",
        callback=Callbacks.enforce_mainnet,
        case_sensitive=False,
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
    network: IcxNetwork = typer.Option(
        Config.get_default_network(),
        "--network",
        "-n",
        callback=Callbacks.enforce_mainnet,
        case_sensitive=False,
    ),
):
    balanced_loans = BalancedLoans(network)

    transaction_result = balanced_loans.liquidate(wallet, address)

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
    network: IcxNetwork = typer.Option(
        Config.get_default_network(),
        "--network",
        "-n",
        callback=Callbacks.enforce_mainnet,
        case_sensitive=False,
    ),
):
    pass


@app.command()
def retire_bnusd(
    amount: int = typer.Argument(...),
    network: IcxNetwork = typer.Option(
        Config.get_default_network(),
        "--network",
        "-n",
        callback=Callbacks.enforce_mainnet,
        case_sensitive=False,
    ),
):
    pass


@app.command()
def swap(
    source_asset: str = typer.Argument(...),
    destination_asset: str = typer.Argument(...),
    network: IcxNetwork = typer.Option(
        Config.get_default_network(),
        "--network",
        "-n",
        callback=Callbacks.enforce_mainnet,
        case_sensitive=False,
    ),
):
    pass


@app.command()
def withdraw(
    keystore: str = typer.Option(
        Config.get_default_keystore(),
        "--keystore",
        "-k",
        callback=Callbacks.load_wallet_from_keystore,
    ),
    amount: str = typer.Argument(0, callback=Callbacks.validate_transaction_value),
    network: IcxNetwork = typer.Option(
        Config.get_default_network(),
        "--network",
        "-n",
        callback=Callbacks.enforce_mainnet,
        case_sensitive=False,
    ),
):
    balanced_loans = BalancedLoans(network)

    transaction_result = balanced_loans.withdraw_collateral(keystore, amount)
    print_tx_hash(transaction_result)
