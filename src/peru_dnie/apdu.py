# Standard Library
from typing import Sequence

# Third Party Library
from attrs import define

ByteLike = Sequence[int] | bytes | bytearray


class APDUError(Exception):
    """Error due from APDU transactions"""


@define
class APDUCommand:
    ins: int
    p1: int
    p2: int
    lc: int | None = None
    data: bytes | None = None
    le: int | None = None
    cla: int = 0x00

    def __attrs_post_init__(self):
        if self.data is None and self.lc is not None:
            raise ValueError("'lc' must be None if 'data' is None")

        elif self.data is not None and self.lc != len(self.data):
            raise ValueError("'lc' must be the length of 'data'")

    def serialize(self) -> bytes:
        command = bytes([self.cla, self.ins, self.p1, self.p2])

        if self.lc is not None and self.data is not None:
            command += self.lc.to_bytes() + self.data

        if self.le is not None:
            command += self.le.to_bytes()

        return command


@define
class APDUResponse:
    sw1: int
    sw2: int
    data: bytes | None = None

    @property
    def ok(self):
        return (self.sw1, self.sw2) == (0x90, 0x00)
