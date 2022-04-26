import typer


def die(message: str, level: str = None):
    if level == "error":
        fg = "red"
        prefix = "ERROR: "
    elif level == "warning":
        fg = "orange"
        prefix = "WARNING: "
    else:
        fg = None
        prefix = None
    typer.secho(f"{prefix}{message}", fg=fg)
    raise typer.Exit()


def format(value: int, exa: int, round: int = 0):
    if round == 0:
        return f"{value / 10**exa}"
    else:
        return f"{round(value / 10**exa, round)}"


def hex_to_int(input: str):
    return int(input, 16)
