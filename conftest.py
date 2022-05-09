import pytest

@pytest.fixture(scope="session")
def test_fixture1():
    print("Run Once")
    return 1