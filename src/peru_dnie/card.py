# Standard Library
from abc import ABC, abstractmethod

# Third Party Library
from attrs import define
from smartcard.pcsc.PCSCReader import PCSCCardConnection

# First Party Library
from peru_dnie.apdu import APDUCommand, APDUResponse


@define
class SmartCard(ABC):
    connection: PCSCCardConnection

    @abstractmethod
    def transmit(self, command: APDUCommand) -> APDUResponse:
        pass
