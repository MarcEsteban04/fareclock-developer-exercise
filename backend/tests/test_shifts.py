"""
Tests for shifts endpoints
"""

import pytest
from datetime import datetime, timedelta


def test_create_shift(client):
    """Test creating a shift"""
    # Create a worker first
    worker_response = client.post("/api/workers", json={"name": "Shift Worker"})
    worker_id = worker_response.json()["id"]
    
    # Create a shift
    start = (datetime.utcnow() + timedelta(hours=1)).isoformat() + "Z"
    end = (datetime.utcnow() + timedelta(hours=9)).isoformat() + "Z"
    
    response = client.post("/api/shifts", json={
        "worker_id": worker_id,
        "start": start,
        "end": end
    })
    assert response.status_code == 201
    data = response.json()
    assert data["worker_id"] == worker_id
    assert "duration" in data
    assert data["duration"] > 0


def test_create_shift_invalid_duration(client):
    """Test creating a shift that exceeds 12 hours"""
    # Create a worker
    worker_response = client.post("/api/workers", json={"name": "Test Worker"})
    worker_id = worker_response.json()["id"]
    
    # Create a shift longer than 12 hours
    start = datetime.utcnow().isoformat() + "Z"
    end = (datetime.utcnow() + timedelta(hours=13)).isoformat() + "Z"
    
    response = client.post("/api/shifts", json={
        "worker_id": worker_id,
        "start": start,
        "end": end
    })
    assert response.status_code == 400
    assert "exceeds maximum" in response.json()["detail"].lower()


def test_create_overlapping_shifts(client):
    """Test that overlapping shifts are rejected"""
    # Create a worker
    worker_response = client.post("/api/workers", json={"name": "Test Worker"})
    worker_id = worker_response.json()["id"]
    
    # Create first shift
    start1 = datetime.utcnow().isoformat() + "Z"
    end1 = (datetime.utcnow() + timedelta(hours=8)).isoformat() + "Z"
    
    response1 = client.post("/api/shifts", json={
        "worker_id": worker_id,
        "start": start1,
        "end": end1
    })
    assert response1.status_code == 201
    
    # Try to create overlapping shift
    start2 = (datetime.utcnow() + timedelta(hours=4)).isoformat() + "Z"
    end2 = (datetime.utcnow() + timedelta(hours=12)).isoformat() + "Z"
    
    response2 = client.post("/api/shifts", json={
        "worker_id": worker_id,
        "start": start2,
        "end": end2
    })
    assert response2.status_code == 400
    assert "overlap" in response2.json()["detail"].lower()


def test_get_shifts(client):
    """Test getting all shifts"""
    # Create a worker and shift
    worker_response = client.post("/api/workers", json={"name": "Test Worker"})
    worker_id = worker_response.json()["id"]
    
    start = datetime.utcnow().isoformat() + "Z"
    end = (datetime.utcnow() + timedelta(hours=8)).isoformat() + "Z"
    client.post("/api/shifts", json={
        "worker_id": worker_id,
        "start": start,
        "end": end
    })
    
    response = client.get("/api/shifts")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_shifts_filtered_by_worker(client):
    """Test getting shifts filtered by worker"""
    # Create two workers
    worker1_response = client.post("/api/workers", json={"name": "Worker 1"})
    worker1_id = worker1_response.json()["id"]
    
    worker2_response = client.post("/api/workers", json={"name": "Worker 2"})
    worker2_id = worker2_response.json()["id"]
    
    # Create shifts for both workers
    start = datetime.utcnow().isoformat() + "Z"
    end = (datetime.utcnow() + timedelta(hours=8)).isoformat() + "Z"
    
    client.post("/api/shifts", json={
        "worker_id": worker1_id,
        "start": start,
        "end": end
    })
    
    client.post("/api/shifts", json={
        "worker_id": worker2_id,
        "start": start,
        "end": end
    })
    
    # Get shifts for worker1 only
    response = client.get(f"/api/shifts?worker_id={worker1_id}")
    assert response.status_code == 200
    data = response.json()
    assert all(shift["worker_id"] == worker1_id for shift in data)

