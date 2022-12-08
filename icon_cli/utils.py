import typer


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
