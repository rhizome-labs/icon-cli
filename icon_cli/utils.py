import typer
from yarl import URL


class Utils:
    def __init__(self) -> None:
        pass

    @staticmethod
    def die(message: str, level: str = None):
        """
        A function that formats and prints an error message before exiting the program.
        """
        # Set color and prefix for die message.
        if level == "error":
            fg = "red"
            prefix = "ERROR: "
        elif level == "warning":
            fg = "orange"
            prefix = "WARNING: "
        else:
            fg = None
            prefix = None

        # Print die message.
        typer.secho(f"{prefix}{message}", fg=fg)

        # Raise error and exit.
        raise typer.Exit()

    @staticmethod
    def strip_all_whitespace(input: str, force_lowercase: bool):
        """
        A function that strips all whitespace from a string.
        """
        input = input.strip()
        input = input.replace(" ", "")
        # Convert to lowercase if force_lowercase is True.
        if force_lowercase is True:
            input = input.casefold()
        return input

    ###################
    # DATA VALIDATORS #
    ###################

    @staticmethod
    def validate_address(address: str) -> str:
        """
        Returns an ICX wallet or contract address if validation passes.

        Args:
            address: An ICX wallet or contract address.
        """
        try:
            # Convert address to lowercase.
            address = address.casefold()
            # Validate ICX wallet address.
            if len(address) == 42 and address.startswith("hx"):
                return address
            # Validate ICX contract address.
            elif len(address) == 42 and address.startswith("cx"):
                return address
            else:
                # Die if address is not validated successfully.
                Utils.die(f"{address} is not a valid ICX wallet or contract address.", "error")  # fmt: skip
        except:
            # Die if address is not validated successfully.
            Utils.die(f"{address} is not a valid ICX wallet or contract address.", "error")  # fmt: skip

    @staticmethod
    def validate_tx_hash(tx_hash: str) -> str:
        """
        Returns an ICX transaction hash if validation passes.

        Args:
            tx_hash: An ICX transaction hash.
        """
        # Convert transaction hash to lowercase.
        tx_hash = tx_hash.casefold()
        # Validate ICX transaction hash.
        if len(tx_hash) == 66 and tx_hash.startswith("0x"):
            return tx_hash
        else:
            # Die if address is not validated successfully.
            Utils.die(f"{tx_hash} is not a valid ICX transaction hash.", "error")  # fmt: skip

    @staticmethod
    def validate_url(url: str) -> str:
        try:
            URL(url)
            return url
        except:
            Utils.die(f"{url} is not a valid HTTP URL.", "error")
