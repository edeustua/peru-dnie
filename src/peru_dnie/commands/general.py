# Standard Library
from typing import Final

# Third Party Library
from rich.prompt import Prompt

# First Party Library
from peru_dnie.apdu import APDUCommand
from peru_dnie.context import Context

SELECT_PKI_APP: Final = APDUCommand(
    cla=0x00,
    ins=0xA4,
    p1=0x04,
    p2=0x00,
    lc=0x0E,
    data=bytes(
        [
            0xE8,
            0x28,
            0xBD,
            0x08,
            0x0F,
            0xD2,
            0x50,
            0x47,
            0x65,
            0x6E,
            0x65,
            0x72,
            0x69,
            0x63,
        ]
    ),
)


def verify_pin(ctx: Context) -> bool:
    """Verify the PIN before a DNIe cryptographic operation"""
    pin = Prompt.ask("Please enter your PIN", password=True)

    encoded_pin = pin.encode("ascii")

    verify_command = APDUCommand(
        cla=0x00,
        ins=0x20,
        p1=0x00,
        p2=0x81,
        lc=len(encoded_pin),
        data=encoded_pin,
    )

    r = ctx.transmit(verify_command)

    if not r.ok:
        raise RuntimeError(f"Failed to verify PIN: '{r:!r}'")

    return True
