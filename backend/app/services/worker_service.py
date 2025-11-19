"""
Worker service for CRUD operations
"""

from google.cloud import datastore
from app.core.datastore import get_datastore_client, KIND_WORKER
from app.models.entities import WorkerEntity
from typing import List, Optional
from datetime import datetime
import uuid


class WorkerService:
    """Service for managing workers"""
    
    def __init__(self):
        self.client = get_datastore_client()
    
    def create_worker(self, name: str) -> dict:
        """Create a new worker"""
        worker_id = str(uuid.uuid4())
        key = self.client.key(KIND_WORKER, worker_id)
        
        entity = WorkerEntity.from_dict({
            "id": worker_id,
            "name": name,
        }, key)
        
        self.client.put(entity)
        return WorkerEntity.to_dict(entity)
    
    def get_worker(self, worker_id: str) -> Optional[dict]:
        """Get a worker by ID"""
        key = self.client.key(KIND_WORKER, worker_id)
        entity = self.client.get(key)
        
        if entity:
            return WorkerEntity.to_dict(entity)
        return None
    
    def get_all_workers(self) -> List[dict]:
        """Get all workers"""
        query = self.client.query(kind=KIND_WORKER)
        query.order = ["name"]
        
        entities = list(query.fetch())
        return [WorkerEntity.to_dict(entity) for entity in entities]
    
    def update_worker(self, worker_id: str, name: str) -> Optional[dict]:
        """Update a worker"""
        key = self.client.key(KIND_WORKER, worker_id)
        entity = self.client.get(key)
        
        if not entity:
            return None
        
        entity.update({
            "name": name,
            "updated_at": datetime.utcnow(),
        })
        
        self.client.put(entity)
        return WorkerEntity.to_dict(entity)
    
    def delete_worker(self, worker_id: str) -> bool:
        """Delete a worker"""
        key = self.client.key(KIND_WORKER, worker_id)
        entity = self.client.get(key)
        
        if not entity:
            return False
        
        self.client.delete(key)
        return True

