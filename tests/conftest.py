from pathlib import Path

import pytest

ROOT = Path(__file__).parent


@pytest.fixture
def data_dir():
    return ROOT / "data"
