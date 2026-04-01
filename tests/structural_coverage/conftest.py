import pytest

from App.Tax_Calculator import TaxEngine


@pytest.fixture
def engine():
    return TaxEngine()
