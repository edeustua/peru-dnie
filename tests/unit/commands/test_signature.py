# Standard Library
from unittest.mock import MagicMock

# Third Party Library
import pytest

# First Party Library
from peru_dnie.commands import general
from peru_dnie.commands.signature import (
    PaddingSchemes,
    build_signature_payload,
    sign_bytes,
)
from peru_dnie.hashes import HashFunction


@pytest.mark.pointer(target=build_signature_payload)
def test_build_signature_payload():
    input_bytes = b"some information to sign"
    hash_sha256 = HashFunction(name="sha256")

    digest_info = build_signature_payload(
        input_bytes, hash_sha256, PaddingSchemes.PKCS1_15
    )

    assert digest_info == (
        hash_sha256.der_encoding()
        + bytes.fromhex(
            "0a409cc96995251f8ed39b45d1eabd159355a03f2f6784fe945d1c824804a8f3"
        )
    )


@pytest.mark.pointer(target=sign_bytes)
def test_sign_bytes(ctx):
    input_bytes = b"some information to sign"

    class FakePrompt:
        ask = MagicMock(return_value="1234")

    general.Prompt = FakePrompt

    signature = sign_bytes(ctx, input_bytes)

    assert signature == b"\xff" * 10
