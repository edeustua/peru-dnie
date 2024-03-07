# Standard Library
from argparse import ArgumentParser
from pathlib import Path
from typing import get_args

# First Party Library
from peru_dnie.card_init import initialize_smart_card
from peru_dnie.commands.certificate import extract_certificate_to_file
from peru_dnie.commands.signature import sign_file
from peru_dnie.context import Context
from peru_dnie.hashes import HashFunction, HashTypes
from peru_dnie.i18n import t


def register_sign_parser(subparsers):
    sign_parser = subparsers.add_parser(
        "sign",
        help=t["cli"]["sign"]["sign_help"],
    )
    sign_parser.add_argument(
        "input_file",
        type=Path,
        help=t["cli"]["sign"]["input_file_help"],
    )
    sign_parser.add_argument(
        "output_file",
        type=Path,
        help=t["cli"]["sign"]["output_file_help"],
    )
    sign_parser.add_argument(
        "--hash-algorithm",
        default="sha256",
        choices=get_args(HashTypes),
        help=t["cli"]["sign"]["hash_algorithm_help"],
    )


def register_extract_certificate_parser(subparsers):
    certificate_parser = subparsers.add_parser(
        "extract",
        help=t["cli"]["extract"]["extract_help"],
    )
    certificate_parser.add_argument(
        "certificate_type",
        choices=["signature", "encryption"],
        type=str,
        help=t["cli"]["extract"]["certificate_type_help"],
    )
    certificate_parser.add_argument(
        "output_file",
        type=Path,
        help=t["cli"]["extract"]["output_file_help"],
    )


def main():
    parser = ArgumentParser(
        prog="dniectl",
        description=t["cli"]["program_description"],
    )

    subparsers = parser.add_subparsers(
        dest="command",
        help=t["cli"]["available_tasks"],
    )

    register_sign_parser(subparsers)
    register_extract_certificate_parser(subparsers)

    args = parser.parse_args()

    if args.command == "sign":
        ctx = Context(hash_func=HashFunction(name=args.hash_algorithm))
        initialize_smart_card(ctx)

        sign_file(
            ctx,
            input_file=args.input_file,
            output_file=args.output_file,
        )

    elif args.command == "extract":
        ctx = Context()
        initialize_smart_card(ctx)

        extract_certificate_to_file(
            ctx,
            output_file=args.output_file,
            certificate_type=args.certificate_type,
        )

    else:
        parser.print_help()
