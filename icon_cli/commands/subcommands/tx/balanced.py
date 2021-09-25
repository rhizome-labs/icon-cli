import typer
from icon_cli.dapps.balanced.Balanced import BalancedCollateralAsset
from icon_cli.dapps.balanced.BalancedLoans import BalancedLoans
from icon_cli.dapps.balanced.BalancedDividends import BalancedDividends
from icon_cli.dapps.balanced.BalancedGovernance import BalancedGovernance
from icon_cli.icx import IcxNetwork
from icon_cli.callbacks import Callbacks
from icon_cli.config import Config
from icon_cli.utils import (
    die,
    format_number_display,
    log,
    print_object,
    print_tx_hash,
    to_loop,
)
from rich import print
from time import sleep

app = typer.Typer()


@app.command()
def debug():
    print_object(__name__)


@app.command()
def borrow(
    borrow_amount: str = typer.Argument(
        0, callback=Callbacks.validate_transaction_value),
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
):

    # Exit if borrow_amount is 0 and --max is False.
    if borrow_amount == 0 and max is False:
        die("Sorry, borrow amount must be greater than 0 bnUSD.")

    balanced_loans = BalancedLoans(network)

    LOCK_THRESHOLD = 0.34

    balanced_position = balanced_loans.query_position_from_address(
        keystore.get_address())
    collateral = balanced_position["assets"]["sICX"]
    collateral_value = collateral * balanced_loans.query_icx_usd_price() / 10 ** 18
    max_borrow_amount = collateral_value * LOCK_THRESHOLD

    if max is True:
        borrow_amount = max_borrow_amount

    log(f"Borrow Amount: {format_number_display(borrow_amount, 18, 18)} bnUSD")
    log(f"Collateral: {format_number_display(collateral, 18, 18)} sICX")
    log(f"Collateral Value: {format_number_display(collateral_value, 0, 18)} USD")
    log(f"Max Borrow Amount: {format_number_display(max_borrow_amount, 18, 18)} bnUSD")

    # Raise exception if borrow_amount is greater than max_borrow_amount.
    if borrow_amount > max_borrow_amount:
        print(
            f"Sorry, you don't have enough collateral to borrow {format_number_display(borrow_amount, 18, 8)} bnUSD.\n"
            f"Your maximum loan size is {format_number_display(max_borrow_amount, 18, 2)} bnUSD."
        )
        die()

    transaction_result = balanced_loans.borrow_bnusd(
        keystore, to_loop(borrow_amount))

    print_tx_hash(transaction_result)


@app.command()
def repay():
    pass


@app.command()
def deposit(
    asset: BalancedCollateralAsset = typer.Argument(..., case_sensitive=False),
    amount: str = typer.Argument(
        0, callback=Callbacks.validate_transaction_value),
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

    if amount <= 0:
        die("Sorry, you need to deposit more than 0 ICX.")

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
        sicx_balance = balanced_loans.query_token_balance(
            keystore.get_address(), "SICX")

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
def evaluate_vote(
    vote_index: int = typer.Argument(...),
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
    balanced_governance = BalancedGovernance(network)
    transaction_result = balanced_governance.evaluate_vote(wallet, vote_index)
    print_tx_hash(transaction_result)


@app.command()
def liquidate(
    address: str = typer.Argument(...,
                                  callback=Callbacks.validate_icx_address),
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
def execute_vote(
    vote_index: int = typer.Argument(...),
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
    balanced_gov = BalancedGovernance(network)

    transaction_result = balanced_gov.execute_vote(keystore, vote_index)
    print_tx_hash(transaction_result)


@app.command()
def rebalance(
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
    loop: bool = typer.Option(False, "--loop", "-l")
):
    balanced_loans = BalancedLoans(network)

    if loop is True:
        while True:
            transaction_result = balanced_loans.rebalance(
                keystore, verify_transaction=False)
            print(transaction_result)
            sleep(0.5)
    else:
        transaction_result = balanced_loans.rebalance(keystore)
        print_tx_hash(transaction_result)


@app.command()
def withdraw(
    keystore: str = typer.Option(
        Config.get_default_keystore(),
        "--keystore",
        "-k",
        callback=Callbacks.load_wallet_from_keystore,
    ),
    amount: str = typer.Argument(
        0, callback=Callbacks.validate_nonzero_transaction_value),
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
