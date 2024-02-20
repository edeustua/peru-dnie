# Third Party Library
from rich.prompt import IntPrompt
from rich.status import Status
from smartcard.CardRequest import CardRequest
from smartcard.CardType import ATRCardType
from smartcard.pcsc.PCSCReader import PCSCCardConnection, PCSCReader
from smartcard.System import readers
from smartcard.util import toHexString

# First Party Library
from peru_dnie.apdu import APDUCommand, APDUResponse
from peru_dnie.cli_config import CLI_CONFIG
from peru_dnie.constants import PERU_DNIE_V2_ATR


class SmartCard:
    def __init__(self):
        self.connection = get_card_connection()
        self.connection.connect()

    def transmit(self, command: APDUCommand) -> APDUResponse:
        serial_bytes = command.serialize()
        data, sw1, sw2 = self.connection.transmit(list(serial_bytes))
        return APDUResponse(sw1=sw1, sw2=sw2, data=bytes(data))


def get_reader_connection() -> PCSCReader:
    """Get connection to the Smart Card reader"""
    current_readers = readers()

    CLI_CONFIG.console.print("[bold underline]Readers:")

    for idx, reader in enumerate(current_readers):
        CLI_CONFIG.console.print(f"[blue]{idx + 1}.[/] {reader}")

    idx = IntPrompt.ask("Choose a reader") - 1

    connection = current_readers[idx].createConnection()
    connection.connect()
    CLI_CONFIG.console.print("ATR:", toHexString(connection.getATR()))

    return connection


def get_card_connection() -> PCSCCardConnection:
    """Get DNIe card connection.

    Wait until the DNIe is connected to the reader and return a connection.
    """
    spinner = Status("Waiting for DNIe...", console=CLI_CONFIG.console)
    spinner.start()

    card_request = CardRequest(timeout=120, cardType=ATRCardType(PERU_DNIE_V2_ATR))
    card_service = card_request.waitforcard()

    if card_service is not None:
        spinner.stop()
        CLI_CONFIG.console.print("[green]Found DNIe V2")

        return card_service.connection
    else:
        raise RuntimeError("Could not find DNIe")
