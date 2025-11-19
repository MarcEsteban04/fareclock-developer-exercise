"""
Tests for workers endpoints
"""

import pytest


def test_create_worker(client):
    """Test creating a worker"""
    response = client.post("/api/workers", json={"name": "John Doe"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "John Doe"
    assert "id" in data


def test_get_workers(client):
    """Test getting all workers"""
    # Create a worker first
    client.post("/api/workers", json={"name": "Jane Doe"})
    
    response = client.get("/api/workers")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_worker(client):
    """Test getting a specific worker"""
    # Create a worker
    create_response = client.post("/api/workers", json={"name": "Test Worker"})
    worker_id = create_response.json()["id"]
    
    # Get the worker
    response = client.get(f"/api/workers/{worker_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Worker"
    assert data["id"] == worker_id


def test_update_worker(client):
    """Test updating a worker"""
    # Create a worker
    create_response = client.post("/api/workers", json={"name": "Old Name"})
    worker_id = create_response.json()["id"]
    
    # Update the worker
    response = client.put(f"/api/workers/{worker_id}", json={"name": "New Name"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New Name"


def test_delete_worker(client):
    """Test deleting a worker"""
    # Create a worker
    create_response = client.post("/api/workers", json={"name": "To Delete"})
    worker_id = create_response.json()["id"]
    
    # Delete the worker
    response = client.delete(f"/api/workers/{worker_id}")
    assert response.status_code == 204
    
    # Verify it's deleted
    response = client.get(f"/api/workers/{worker_id}")
    assert response.status_code == 404

