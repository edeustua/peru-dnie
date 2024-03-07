# Standard Library
from enum import Enum
from pathlib import Path

# First Party Library
from peru_dnie.apdu import APDUCommand, APDUError
from peru_dnie.context import Context
from peru_dnie.hashes import HashFunction
from peru_dnie.i18n import t

# Local Modules
from .general import SELECT_PKI_APP, PinType, verify_pin


class PaddingSchemes(str, Enum):
    PKCS1_15 = "pkcs1_15"


def build_signature_payload(
    input_bytes: bytes,
    hash_func: HashFunction,
    padding_scheme: PaddingSchemes,
) -> bytes:
    """Prepare a PKCS padded sha256sum hash

    Source <https://datatracker.ietf.org/doc/html/rfc3447#section-9.2>

    Peruvian DNIe v2 is configured for padding the digest info payload. There is no need
    for filling with 0x00 0x01 0xff.. 0xff 0x00 digest_info.
    """

    hashed_bytes = hash_func(input_bytes)
    if padding_scheme == PaddingSchemes.PKCS1_15:
        digest_info = hash_func.der_encoding() + hashed_bytes
    else:
        raise TypeError("Padding scheme not supported")

    return digest_info


def sign_bytes(
    ctx: Context,
    input_bytes: bytes,
) -> bytes:
    """Sign a string of bytes with the DNIe card."""

    if ctx.hash_func is None:
        raise ValueError("A hash function is needed for a signature.")

    pkcs1_15_padded_hash = build_signature_payload(
        input_bytes,
        ctx.hash_func,
        PaddingSchemes.PKCS1_15,
    )

    r = ctx.transmit(SELECT_PKI_APP)

    if not r.ok:
        raise APDUError(t["errors"]["could_not_select_pki"].format(repr(r)))

    verify_pin(ctx, pin_type=PinType.SIGNATURE)

    # Set security enviroment for RSA signature, off-card hashing, and in card
    # padding. With these settings the card expects a hash with its corresponding
    # digest_info hash identifier. The padding bytes are added by the card.
    set_security_environment = APDUCommand(
        cla=0x00,
        ins=0x22,
        p1=0x41,
        p2=0xB6,
        lc=0x06,
        data=bytes(
            [
                0x80,
                0x01,
                0x8A,
                0x84,
                0x01,
                0x81,
            ]
        ),
    )

    r = ctx.transmit(set_security_environment)

    if not r.ok:
        raise APDUError(t["errors"]["could_not_set_env"].format(repr(r)))

    signature_command = APDUCommand(
        cla=0x00,
        ins=0x2A,
        p1=0x9E,
        p2=0x9A,
        lc=len(pkcs1_15_padded_hash),
        data=pkcs1_15_padded_hash,
    )

    r = ctx.transmit(signature_command)

    if not r.ok or r.data is None:
        raise APDUError(t["errors"]["could_not_sign"].format(repr(r)))

    return r.data


def sign_file(
    ctx: Context,
    *,
    input_file: Path,
    output_file: Path,
) -> None:
    """Sign a file with the DNIe"""

    input_bytes = input_file.read_bytes()

    signature = sign_bytes(ctx, input_bytes)

    output_file.write_bytes(signature)
