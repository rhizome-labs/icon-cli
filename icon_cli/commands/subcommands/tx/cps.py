import typer
from icon_cli.callbacks import Callbacks
from icon_cli.config import Config
<<<<<<< Updated upstream
from icon_cli.icx import Icx, IcxNetwork
from icon_cli.utils import die, print_object
from rich import print
=======
from icon_cli.cps import Cps
from icon_cli.utils import die
from icon_cli.validators import Validators
>>>>>>> Stashed changes

app = typer.Typer()


@app.command()
def debug():
    print_object(__name__)

@app.command()
def vote():
    pass