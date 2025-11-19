"""
Tests for timezone endpoints
"""

import pytest
from app.services.timezone_service import TimezoneService


def test_get_default_timezone(client):
    """Test getting default timezone"""
    response = client.get("/api/timezone")
    assert response.status_code == 200
    data = response.json()
    assert "timezone" in data
    assert data["timezone"] == "UTC"  # Default


def test_set_timezone(client):
    """Test setting timezone"""
    response = client.post("/api/timezone", json={"timezone": "America/New_York"})
    assert response.status_code == 200
    data = response.json()
    assert data["timezone"] == "America/New_York"
    
    # Verify it was saved
    response = client.get("/api/timezone")
    assert response.status_code == 200
    data = response.json()
    assert data["timezone"] == "America/New_York"

