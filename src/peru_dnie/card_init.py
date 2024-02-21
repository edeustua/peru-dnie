# Third Party Library
from rich.prompt import IntPrompt
from rich.status import Status

# First Party Library
from peru_dnie.context import Context
from peru_dnie.pyscard import PyscardSmartCard, get_dnie_connection, get_readers


def select_reader(ctx: Context):
    readers = get_readers()

    idx = IntPrompt.ask("Choose a reader", console=ctx.cli.console) - 1

    ctx.cli.console.print("[bold underline]Readers:")
    for idx, reader in enumerate(readers):
        ctx.cli.console.print(f"[blue]{idx + 1}.[/] {reader}")


def initialize_smart_card(ctx: Context):
    spinner = Status("Waiting for DNIe...", console=ctx.cli.console)
    spinner.start()

    ctx.card = PyscardSmartCard(connection=get_dnie_connection())
    ctx.card.connection.connect()

    spinner.stop()
    ctx.cli.console.print("[green]Found DNIe V2")
