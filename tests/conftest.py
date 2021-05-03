import pytest
from fastapi.testclient import TestClient

from cowin_notifier.main import app

@pytest.fixture(scope="module")
def test_app():
    return TestClient(app)
