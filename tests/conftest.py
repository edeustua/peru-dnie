# Third Party Library
import pytest

# First Party Library
from peru_dnie.context import FakeContext
from peru_dnie.hashes import HashFunction


@pytest.fixture(scope="session")
def ctx():
    yield FakeContext(hash_func=HashFunction(name="sha256"))
