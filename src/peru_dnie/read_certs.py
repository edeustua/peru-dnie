import hashlib
from argparse import ArgumentParser
from pathlib import Path
from typing import Final

from attrs import define
from rich.console import Console
from rich.prompt import IntPrompt, Prompt
from rich.status import Status
from smartcard.CardRequest import CardRequest
from smartcard.CardType import ATRCardType
from smartcard.pcsc.PCSCReader import PCSCCardConnection, PCSCReader
from smartcard.System import readers
from smartcard.util import toHexString

# APDU Commands: https://serviciosportal.reniec.gob.pe/static/portal/pdf/manual_comandos_dnie_v2.pdf


@define
class APDU:
    ins: int
    p1: int
    p2: int
    cla: int = 0x00


DEBUG = True

console = Console(color_system="truecolor")

AVAILABLE_COMMANDS: Final = [
    "signing-certificate",
    "sign",
]


MODULUS_SIZE: Final = 256
DER_HASH_ALGORITHM_ENCODINGS: Final = {
    "sha1": bytes(
        [
            0x30,
            0x21,
            0x30,
            0x09,
            0x06,
            0x05,
            0x2B,
            0x0E,
            0x03,
            0x02,
            0x1A,
            0x05,
            0x00,
            0x04,
            0x14,
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
}


DNI_V2_ATR: Final = ATRCardType(
    [
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
)

PKI_APP_SELECT: Final = [
    0x00,
    0xA4,
    0x04,
    0x00,
    0x0E,
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

PKI_APP_SELECT_SIGNATURE_CERTIFICATE: Final = [
    0x00,
    0xA4,
    0x02,
    0x04,
    0x02,
    0x00,
    0x1D,
]

# Needs a length byte and then the PIN appended in ASCII
PKI_APP_VERIFY_PIN: Final = [
    0x00,
    0x20,
    0x00,
    0x81,
]

PKI_APP_SIGN_PREP: Final = [
    0x00,
    0x22,
    0x41,
    0xB6,
    0x06,
    0x80,
    0x01,
    0x8A,
    0x84,
    0x01,
    0x81,
]

# Need a length byte and data appended
PKI_APP_SIGN: Final = [
    0x00,
    0x2A,
    0x9E,
    0x9A,
]


def get_reader_connection() -> PCSCReader:
    """Get connection to the Smart Card reader"""
    current_readers = readers()

    console.print("[bold underline]Readers:")

    for idx, reader in enumerate(current_readers):
        console.print(f"[blue]{idx+1}.[/] {reader}")

    idx = IntPrompt.ask("Choose a reader") - 1

    connection = current_readers[idx].createConnection()
    connection.connect()
    console.print("ATR:", toHexString(connection.getATR()))

    return connection


def get_card_connection() -> PCSCCardConnection:
    """Get DNIe card connection.

    Wait until the DNIe is connected to the reader and return a connection.
    """
    spinner = Status("Waiting for DNIe...", console=console)
    spinner.start()

    card_request = CardRequest(timeout=120, cardType=DNI_V2_ATR)
    card_service = card_request.waitforcard()

    if card_service is not None:
        spinner.stop()
        console.print("[green]Found DNIe V2")

        return card_service.connection
    else:
        raise RuntimeError("Could not find DNIe")


def get_signature_certificate(connection: PCSCCardConnection) -> bytes:
    """Get signature x509 certificate from DNIe"""
    _, sw1, sw2 = connection.transmit(PKI_APP_SELECT)

    if DEBUG:
        print("Select PKI: 0x{:02x}{:02x}".format(sw1, sw2))

    _, sw1, sw2 = connection.transmit(PKI_APP_SELECT_SIGNATURE_CERTIFICATE)
    if DEBUG:
        print("Select signature certificate: 0x{:02x}{:02x}".format(sw1, sw2))

    read_cert_apdu_command = [
        0x00,
        0xB1,
        0x00,
        0x00,
        0x04,
        0x54,
        0x02,
        0x00,
        0x00,
        0xFF,
    ]

    spinner = Status("Reading signature certificate...", console=console)
    spinner.start()

    output = []
    success = False
    while True:
        data, sw1, sw2 = connection.transmit(read_cert_apdu_command)

        # First two bytes are the tag. Third byte is length (should be 0xe4).
        # See TLV frame.
        output += data[3:]
        if DEBUG:
            print("-------------------")
            print("Result {:02x} {:02x}".format(sw1, sw2))
            print("  ", "Data", toHexString(data))
            print("  ", "Offset:", [hex(j) for j in read_cert_apdu_command[-3:-1]])
            print("-------------------\n")

        # Break if Status Word is found
        if (sw1, sw2) == (0x62, 0x82):
            success = True
            break

        if data[0] != 0x53 or (sw1, sw2) != (0x90, 0x00):
            raise RuntimeError(
                "Something went wrong while reading the certificate."
                f" Code: 0x{sw1:02x}{sw2:02x}"
            )

        # Update reading command with new offset
        offset = int.from_bytes(bytes(read_cert_apdu_command[-3:-1]))
        offset += 0xE4
        offset = offset.to_bytes(length=2)
        read_cert_apdu_command[-3:-1] = offset

    if success:
        console.print("[green]Certificate successfully loaded")
    else:
        console.print("[red]Could not read certificate")
        raise RuntimeError("Could not read signature certificate")

    return bytes(output)


def hash_sha256(input_bytes: bytes) -> bytes:
    """Hash the input file for DNIe signature"""
    hash = hashlib.sha256(input_bytes).digest()

    return hash


def hash_sha1(input_bytes: bytes) -> bytes:
    """Hash the input file for DNIe signature"""
    hash = hashlib.sha1(input_bytes).digest()

    return hash


def build_pkcs_padding(digest_info_length: int) -> bytes:
    """Build PKCS padding for DNIe signature"""
    padding_length = MODULUS_SIZE - digest_info_length - 3

    return b"\xff" * padding_length


def build_file_signature_clear_text(input_file: Path) -> bytes:
    """Prepare a PKCS padded sha256sum hash

    Source <https://datatracker.ietf.org/doc/html/rfc3447#section-9.2>

    """

    file_bytes = input_file.read_bytes()
    hashed_bytes = hash_sha256(file_bytes)
    # hashed_bytes = hash_sha1(file_bytes)
    digest_info = DER_HASH_ALGORITHM_ENCODINGS["sha256"] + hashed_bytes
    # padding = build_pkcs_padding(len(digest_info))

    return digest_info


def verify_pin(connection: PCSCCardConnection) -> None:
    """Verify the PIN before a DNIe cryptographic operation"""
    pin = Prompt.ask("Please enter your PIN", password=True)

    encoded_pin = pin.encode("ascii")
    verify_command = PKI_APP_VERIFY_PIN + [len(encoded_pin)] + list(encoded_pin)

    _, sw1, sw2 = connection.transmit(verify_command)

    if (sw1, sw2) != (0x90, 0x00):
        raise RuntimeError(f"Failed to verify PIN: 0x{sw1:02x}{sw2:02x}")


def sign_file(
    connection: PCSCCardConnection,
    *,
    input_file: Path,
    output_file: Path,
) -> None:
    """Sign a file with the DNIe"""

    pkcs_hash = build_file_signature_clear_text(input_file)

    _, sw1, sw2 = connection.transmit(PKI_APP_SELECT)
    if DEBUG:
        print("Select PKI: 0x{:02x}{:02x}".format(sw1, sw2))

    verify_pin(connection)

    _, sw1, sw2 = connection.transmit(PKI_APP_SIGN_PREP)
    if DEBUG:
        print("PKI sign prep: 0x{:02x}{:02x}".format(sw1, sw2))

    pki_sign = PKI_APP_SIGN.copy()
    # print(len(pkcs_hash), pkcs_hash.hex(":"))
    hash_command = pki_sign + [len(pkcs_hash)] + list(pkcs_hash)
    # hash_command = (
    #     pki_sign + [len(input_file.read_bytes())] + list(input_file.read_bytes())
    # )
    data, sw1, sw2 = connection.transmit(hash_command)

    output_file.write_bytes(bytes(data))
    print("Code", "0x{:02x}{:02x}".format(sw1, sw2))
    print("Data", toHexString(data))
    print(len(data))


if __name__ == "__main__":
    parser = ArgumentParser(
        prog="dniectl",
        description=(
            "Utilities for the Peruvian DNIe Smart Card cryptographic functions"
        ),
    )

    subparsers = parser.add_subparsers(
        dest="command",
        help="Available DNIe tasks",
    )

    sign_parser = subparsers.add_parser(
        "sign",
        help="Sign with the DNIe",
    )
    sign_parser.add_argument(
        "input_file",
        type=Path,
        help="File to sign",
    )

    sign_parser.add_argument(
        "output_file",
        type=Path,
        help="File with signature",
    )

    args = parser.parse_args()

    if args.command == "sign":
        connection = get_card_connection()
        connection.connect()
        sign_file(
            connection,
            input_file=args.input_file,
            output_file=args.output_file,
        )
    else:
        parser.print_help()
