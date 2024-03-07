# Standard Library
from typing import Union

# Third Party Library
from attrs import define

# First Party Library
from peru_dnie.apdu import APDUCommand, APDUResponse
from peru_dnie.card import SmartCard
from peru_dnie.cli_config import CLI_CONFIG, CliConfig
from peru_dnie.hashes import HashFunction
from peru_dnie.i18n import t


@define
class Context:
    hash_func: Union[HashFunction, None] = None
    card: Union[SmartCard, None] = None
    cli: CliConfig = CLI_CONFIG

    def transmit(self, command: APDUCommand) -> APDUResponse:
        if self.card is None:
            raise RuntimeError(t["errors"]["dnie_not_init"])
        return self.card.transmit(command)


@define
class FakeContext(Context):
    def transmit(self, command: APDUCommand):
        if command.serialize()[:4] == bytes([0x00, 0x2A, 0x9E, 0x9A]):
            data = b"\xff" * 10
        else:
            data = None
        return APDUResponse(sw1=0x90, sw2=0x00, data=data)
