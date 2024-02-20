# Standard Library
from typing import Sequence, Union

# Third Party Library
from attrs import define

ByteLike = Union[Sequence[int], bytes, bytearray]


class APDUError(Exception):
    """Error due from APDU transactions"""


@define
class APDUCommand:
    ins: int
    p1: int
    p2: int
    lc: Union[int, None] = None
    data: Union[bytes, None] = None
    le: Union[int, None] = None
    cla: int = 0x00

    def __attrs_post_init__(self):
        if self.data is None and self.lc is not None:
            raise ValueError("'lc' must be None if 'data' is None")

        elif self.data is not None and self.lc != len(self.data):
            raise ValueError("'lc' must be the length of 'data'")

    def serialize(self) -> bytes:
        command = bytes([self.cla, self.ins, self.p1, self.p2])

        if self.lc is not None and self.data is not None:
            command += self.lc.to_bytes(length=2, byteorder="big") + self.data

        if self.le is not None:
            command += self.le.to_bytes(length=2, byteorder="big")

        return command


@define
class APDUResponse:
    sw1: int
    sw2: int
    data: Union[bytes, None] = None

    @property
    def ok(self):
        return (self.sw1, self.sw2) == (0x90, 0x00)
