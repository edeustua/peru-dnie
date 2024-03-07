# Standard Library
from typing import List

# Third Party Library
from attrs import define
from smartcard.CardRequest import CardRequest
from smartcard.CardType import ATRCardType
from smartcard.pcsc.PCSCReader import PCSCCardConnection, PCSCReader
from smartcard.System import readers

# First Party Library
from peru_dnie.apdu import APDUCommand, APDUResponse
from peru_dnie.card import SmartCard
from peru_dnie.constants import PERU_DNIE_V2_ATR
from peru_dnie.exceptions import CardError
from peru_dnie.i18n import t


@define
class PyscardSmartCard(SmartCard):
    def transmit(self, command: APDUCommand) -> APDUResponse:
        serial_bytes = command.serialize()
        data, sw1, sw2 = self.connection.transmit(list(serial_bytes))
        return APDUResponse(sw1=sw1, sw2=sw2, data=bytes(data))


def get_readers() -> List[PCSCReader]:
    """Get Smart Card readers"""
    current_readers = readers()
    return current_readers


def get_dnie_connection() -> PCSCCardConnection:
    """Get DNIe card connection.

    Wait until the DNIe is connected to the reader and return a connection.
    """
    card_request = CardRequest(timeout=120, cardType=ATRCardType(PERU_DNIE_V2_ATR))
    card_service = card_request.waitforcard()

    if card_service is not None:
        return card_service.connection
    else:
        raise CardError(t["errors"]["dnie_not_found"])
