# Third Party Library
import pytest

# First Party Library
from peru_dnie.constants import DER_HASH_ALGORITHM_ENCODINGS
from peru_dnie.hashes import (
    HashFunction,
    hash_sha224,
    hash_sha256,
    hash_sha384,
    hash_sha512,
)


class Test_HashFunction:
    @pytest.mark.pointer(target=HashFunction.der_encoding)
    def test_der_encoding(self):
        hash_func = HashFunction(name="sha256")

        assert hash_func.der_encoding() == DER_HASH_ALGORITHM_ENCODINGS["sha256"]

    @pytest.mark.pointer(target=HashFunction.__call__)
    def test___call__(self):
        hash_func = HashFunction(name="sha256")
        some_data = b"some data here"
        hash = hash_func(some_data)

        assert hash == bytes.fromhex(
            "679aa02ff1852e40618b0701f430cad8bfcaa0811579edb17a258c2b322b9826"
        )


@pytest.mark.pointer(target=hash_sha224)
def test_hash_sha224():
    some_data = b"some data here"
    hash = hash_sha224(some_data)

    assert (
        hash
        == b"\x84l\x7fc\xc4\x9d\xb3\xa5}?N\xec\x0e2A\xeb?\xa3\xf9\xd70\xde-A\x98\xd0\xe8\x01"
    )


@pytest.mark.pointer(target=hash_sha256)
def test_hash_sha256():
    some_data = b"some data here"
    hash = hash_sha256(some_data)

    assert hash == bytes.fromhex(
        "679aa02ff1852e40618b0701f430cad8bfcaa0811579edb17a258c2b322b9826"
    )


@pytest.mark.pointer(target=hash_sha384)
def test_hash_sha384():
    some_data = b"some data here"
    hash = hash_sha384(some_data)

    assert hash == bytes.fromhex(
        "82f2d988f9e7acaf5def7a297b159247998e69a7e720bb7a4a1fb77d080731530d97cec50c003e929d72cd1c76baa52c"
    )


@pytest.mark.pointer(target=hash_sha512)
def test_hash_sha512():
    some_data = b"some data here"
    hash = hash_sha512(some_data)

    assert hash == bytes.fromhex(
        "c0b2a5f4e22cf4f23233ac51a47f522aa92ef49647be72eaa8e287fe663707678173c8038c2b3e3a1d870f8ae21b807a9d4917cb5247de10105984f441baf518"
    )
