# Standard Library
from enum import Enum, auto
from typing import Final

MODULUS_SIZE: Final = 256

DER_HASH_ALGORITHM_ENCODINGS: Final = {
    "sha224": bytes(
        [
            0x30,
            0x2D,
            0x30,
            0x0D,
            0x06,
            0x09,
            0x60,
            0x86,
            0x48,
            0x01,
            0x65,
            0x03,
            0x04,
            0x02,
            0x04,
            0x05,
            0x00,
            0x04,
            0x1C,
        ]
    ),
    "sha256": bytes(
        [
            0x30,
            0x31,
            0x30,
            0x0D,
            0x06,
            0x09,
            0x60,
            0x86,
            0x48,
            0x01,
            0x65,
            0x03,
            0x04,
            0x02,
            0x01,
            0x05,
            0x00,
            0x04,
            0x20,
        ]
    ),
    "sha384": bytes(
        [
            0x30,
            0x41,
            0x30,
            0x0D,
            0x06,
            0x09,
            0x60,
            0x86,
            0x48,
            0x01,
            0x65,
            0x03,
            0x04,
            0x02,
            0x02,
            0x05,
            0x00,
            0x04,
            0x30,
        ]
    ),
    "sha512": bytes(
        [
            0x30,
            0x51,
            0x30,
            0x0D,
            0x06,
            0x09,
            0x60,
            0x86,
            0x48,
            0x01,
            0x65,
            0x03,
            0x04,
            0x02,
            0x03,
            0x05,
            0x00,
            0x04,
            0x40,
        ]
    ),
}

PERU_DNIE_V2_ATR: Final = [
    0x3B,
    0xDC,
    0x18,
    0xFF,
    0x81,
    0x91,
    0xFE,
    0x1F,
    0xC3,
    0x80,
    0x73,
    0xC8,
    0x21,
    0x13,
    0x66,
    0x05,
    0x03,
    0x63,
    0x51,
    0x00,
    0x02,
    0x50,
]

PERU_DNIE_V2_ATR_NFC: Final = [
    0x3B,
    0x80,
    0x80,
    0x01,
    0x01,
]


class CertificateType(Enum):
    SIGNATURE = auto()
    AUTHENTICATION = auto()
    ENCRYPTION = auto()


CERTIFICATE_FILE_ID: Final = {
    CertificateType.SIGNATURE: [0x00, 0x1D],
    CertificateType.AUTHENTICATION: [0x00, 0x1C],
    CertificateType.ENCRYPTION: [0x00, 0x1B],
}
