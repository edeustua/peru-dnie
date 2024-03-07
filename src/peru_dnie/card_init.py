# Third Party Library
from rich.prompt import IntPrompt
from rich.status import Status

# First Party Library
from peru_dnie.context import Context
from peru_dnie.i18n import t
from peru_dnie.pyscard import PyscardSmartCard, get_dnie_connection, get_readers


def select_reader(ctx: Context):
    readers = get_readers()

    idx = IntPrompt.ask(t["init"]["choose_reader"], console=ctx.cli.console) - 1

    ctx.cli.console.print(t["init"]["readers"])
    for idx, reader in enumerate(readers):
        ctx.cli.console.print(f"[blue]{idx + 1}.[/] {reader}")


def initialize_smart_card(ctx: Context):
    spinner = Status(t["init"]["waiting_dnie"], console=ctx.cli.console)
    spinner.start()

    ctx.card = PyscardSmartCard(connection=get_dnie_connection())
    ctx.card.connection.connect()

    spinner.stop()
    ctx.cli.console.print(t["init"]["found_dnie"])
