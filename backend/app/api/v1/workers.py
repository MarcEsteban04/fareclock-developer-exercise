"""
Workers API endpoints
"""

from fastapi import APIRouter, HTTPException
from typing import List
from app.models.schemas import Worker, WorkerCreate, WorkerUpdate, ErrorResponse
from app.services.worker_service import WorkerService

router = APIRouter()
worker_service = WorkerService()


@router.get("", response_model=List[Worker])
async def get_workers():
    """Get all workers"""
    try:
        workers = worker_service.get_all_workers()
        return workers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{worker_id}", response_model=Worker)
async def get_worker(worker_id: str):
    """Get a worker by ID"""
    try:
        worker = worker_service.get_worker(worker_id)
        if not worker:
            raise HTTPException(status_code=404, detail="Worker not found")
        return worker
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=Worker, status_code=201)
async def create_worker(worker: WorkerCreate):
    """Create a new worker"""
    try:
        created = worker_service.create_worker(worker.name)
        return created
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{worker_id}", response_model=Worker)
async def update_worker(worker_id: str, worker: WorkerUpdate):
    """Update a worker"""
    try:
        updated = worker_service.update_worker(worker_id, worker.name)
        if not updated:
            raise HTTPException(status_code=404, detail="Worker not found")
        return updated
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{worker_id}", status_code=204)
async def delete_worker(worker_id: str):
    """Delete a worker"""
    try:
        deleted = worker_service.delete_worker(worker_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Worker not found")
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

