# Standard Library
from argparse import ArgumentParser
from pathlib import Path
from typing import get_args

# First Party Library
from peru_dnie.commands.certificate import extract_certificate_to_file
from peru_dnie.commands.signature import sign_file
from peru_dnie.context import Context
from peru_dnie.hashes import HashFunction, HashTypes


def register_sign_parser(subparsers):
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
    sign_parser.add_argument(
        "--hash-algorithm",
        default="sha256",
        choices=get_args(HashTypes),
        help="Hash algorithm for the signature",
    )


def register_extract_certificate_parser(subparsers):
    certificate_parser = subparsers.add_parser(
        "extract",
        help="Extract certificates from the DNIe",
    )
    certificate_parser.add_argument(
        "certificate_type",
        choices=["signature", "encryption"],
        type=str,
        help="Type of certificate to extract",
    )
    certificate_parser.add_argument(
        "output_file",
        type=Path,
        help="File to write the certificate to",
    )


def main():
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

    register_sign_parser(subparsers)
    register_extract_certificate_parser(subparsers)

    args = parser.parse_args()

    if args.command == "sign":
        ctx = Context(hash_func=HashFunction(name=args.hash_algorithm))
        ctx.initialize()

        sign_file(
            ctx,
            input_file=args.input_file,
            output_file=args.output_file,
        )
    elif args.command == "extract":
        ctx = Context()
        ctx.initialize()

        extract_certificate_to_file(
            ctx,
            output_file=args.output_file,
            certificate_type=args.certificate_type,
        )
    else:
        parser.print_help()
