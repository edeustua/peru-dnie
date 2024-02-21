# Standard Library
from pathlib import Path

# Third Party Library
from rich.status import Status

# First Party Library
from peru_dnie.apdu import APDUCommand, APDUError
from peru_dnie.context import Context

# Local Modules
from .general import SELECT_PKI_APP


def extract_signature_certificate(ctx: Context) -> bytes:
    """Get signature x509 certificate from DNIe"""

    # Open PKI app
    r = ctx.transmit(SELECT_PKI_APP)

    if ctx.cli.DEBUG:
        print("Select PKI: '{r:!r}'")

    if not r.ok:
        raise APDUError(f"Could not select PKI app: '{r:!r}'")

    # Select signature certificate
    select_signature_certificate = APDUCommand(
        cla=0x00,
        ins=0xA4,
        p1=0x02,
        p2=0x04,
        lc=0x02,
        data=bytes([0x00, 0x1D]),
    )
    r = ctx.transmit(select_signature_certificate)

    if ctx.cli.DEBUG:
        print("Select signature certificate: '{r:!r}'")

    if not r.ok:
        raise APDUError(f"Could not select signature certificate file: '{r:!r}'")

    read_cert_apdu_command = APDUCommand(
        cla=0x00,
        ins=0xB1,
        p1=0x00,
        p2=0x00,
        lc=0x04,
        data=bytes([0x54, 0x02, 0x00, 0x00]),
        le=0xFF,
    )

    if read_cert_apdu_command.data is None:
        raise TypeError(
            f"Read certificate data APDU must have a data field '{read_cert_apdu_command:!r}'"
        )

    spinner = Status("Reading signature certificate...", console=ctx.cli.console)
    spinner.start()

    output_certificate = b""
    success = False
    while True:
        r = ctx.transmit(read_cert_apdu_command)

        if r.data is None:
            raise APDUError(f"Could not read signature certificate '{r:!r}'")

        # First two bytes are the tag. Third byte is length (should be 0xe4).
        # See TLV frame.
        output_certificate += r.data[3:]

        if ctx.cli.DEBUG:
            print("-------------------")
            print(f"Response '{r:!r}'")
            print("  ", "Data", r.data)
            print("  ", "Offset:", [hex(j) for j in read_cert_apdu_command.data])
            print("-------------------\n")

        # Break if Status Word is found
        if (r.sw1, r.sw2) == (0x62, 0x82):
            success = True
            break

        if r.data[0] != 0x53 or not r.ok:
            raise APDUError(
                f"Something went wrong while reading the certificate: '{r:!r}'"
            )

        # Update reading command with new offset
        offset = int.from_bytes(read_cert_apdu_command.data[2:]) + 0xE4
        offset = offset.to_bytes(length=2, byteorder="big")
        read_cert_apdu_command.data = read_cert_apdu_command.data[:2] + offset

    if success:
        spinner.stop()
        ctx.cli.console.print("[green]Certificate successfully loaded")
    else:
        ctx.cli.console.print("[red]Could not read certificate")
        raise RuntimeError("Could not read signature certificate")

    return output_certificate


def extract_certificate_to_file(
    ctx: Context,
    *,
    output_file: Path,
    certificate_type: str,
):
    if certificate_type == "signature":
        certificate = extract_signature_certificate(ctx)
    else:
        raise TypeError("Certificate type extraction not supported")

    output_file.write_bytes(certificate)
    ctx.cli.console.print(f"[green]Wrote certificate to '{output_file.name}'")
