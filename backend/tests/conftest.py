"""
Pytest configuration and fixtures
"""

import pytest
import os
from fastapi.testclient import TestClient
from app.main import app

# Set up Datastore emulator for tests
os.environ["DATASTORE_EMULATOR_HOST"] = "localhost:8081"
os.environ["GCP_PROJECT_ID"] = "test-project"


@pytest.fixture
def client():
    """Test client fixture"""
    return TestClient(app)


@pytest.fixture
def datastore_client():
    """Datastore client fixture"""
    from app.core.datastore import get_datastore_client
    return get_datastore_client()

