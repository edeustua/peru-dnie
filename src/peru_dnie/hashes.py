# Standard Library
import hashlib
from typing import Literal

# Third Party Library
from attrs import define

# First Party Library
from peru_dnie.constants import DER_HASH_ALGORITHM_ENCODINGS

HashTypes = Literal["sha224", "sha256", "sha384", "sha512"]


@define
class HashFunction:
    name: HashTypes

    def der_encoding(self) -> bytes:
        return DER_HASH_ALGORITHM_ENCODINGS[self.name]

    def __call__(self, input_bytes: bytes) -> bytes:
        if self.name == "sha224":
            return hash_sha224(input_bytes)
        elif self.name == "sha256":
            return hash_sha256(input_bytes)
        elif self.name == "sha384":
            return hash_sha384(input_bytes)
        elif self.name == "sha512":
            return hash_sha384(input_bytes)
        else:
            raise TypeError("Hash function not supported")


def hash_sha224(input_bytes: bytes) -> bytes:
    """Hash the input file for DNIe signature"""
    hash = hashlib.sha224(input_bytes).digest()

    return hash


def hash_sha256(input_bytes: bytes) -> bytes:
    """Hash the input file for DNIe signature"""
    hash = hashlib.sha256(input_bytes).digest()

    return hash


def hash_sha384(input_bytes: bytes) -> bytes:
    """Hash the input file for DNIe signature"""
    hash = hashlib.sha384(input_bytes).digest()

    return hash


def hash_sha512(input_bytes: bytes) -> bytes:
    """Hash the input file for DNIe signature"""
    hash = hashlib.sha512(input_bytes).digest()

    return hash
