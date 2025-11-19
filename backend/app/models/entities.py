"""
Datastore entity models and utilities
"""

from google.cloud import datastore
from datetime import datetime
from typing import Optional
from app.core.datastore import KIND_WORKER, KIND_SHIFT, KIND_TIMEZONE


def calculate_duration(start_iso: str, end_iso: str) -> float:
    """
    Calculate duration between two ISO 8601 datetime strings in hours.
    Returns floating point hours.
    """
    start = datetime.fromisoformat(start_iso.replace('Z', '+00:00'))
    end = datetime.fromisoformat(end_iso.replace('Z', '+00:00'))
    delta = end - start
    return delta.total_seconds() / 3600.0


class WorkerEntity:
    """Worker entity model"""
    
    @staticmethod
    def to_dict(entity: datastore.Entity) -> dict:
        """Convert Datastore entity to dictionary"""
        return {
            "id": entity.key.id_or_name,
            "name": entity.get("name", ""),
            "created_at": entity.get("created_at"),
            "updated_at": entity.get("updated_at"),
        }
    
    @staticmethod
    def from_dict(data: dict, key: Optional[datastore.Key] = None) -> datastore.Entity:
        """Create Datastore entity from dictionary"""
        if key is None:
            key = datastore.Key(KIND_WORKER, data.get("id"))
        
        entity = datastore.Entity(key=key)
        entity.update({
            "name": data["name"],
            "created_at": data.get("created_at", datetime.utcnow()),
            "updated_at": datetime.utcnow(),
        })
        return entity


class ShiftEntity:
    """Shift entity model"""
    
    @staticmethod
    def to_dict(entity: datastore.Entity) -> dict:
        """Convert Datastore entity to dictionary"""
        start_iso = entity.get("start")
        end_iso = entity.get("end")
        duration = calculate_duration(start_iso, end_iso) if start_iso and end_iso else 0.0
        
        return {
            "id": entity.key.id_or_name,
            "worker_id": entity.get("worker_id", ""),
            "start": start_iso,
            "end": end_iso,
            "duration": duration,
            "created_at": entity.get("created_at"),
            "updated_at": entity.get("updated_at"),
        }
    
    @staticmethod
    def from_dict(data: dict, key: Optional[datastore.Key] = None) -> datastore.Entity:
        """Create Datastore entity from dictionary"""
        if key is None:
            key = datastore.Key(KIND_SHIFT, data.get("id"))
        
        start_iso = data["start"]
        end_iso = data["end"]
        
        entity = datastore.Entity(key=key)
        entity.update({
            "worker_id": data["worker_id"],
            "start": start_iso,
            "end": end_iso,
            "created_at": data.get("created_at", datetime.utcnow()),
            "updated_at": datetime.utcnow(),
        })
        return entity


class TimezoneEntity:
    """Timezone setting entity model"""
    
    @staticmethod
    def to_dict(entity: datastore.Entity) -> dict:
        """Convert Datastore entity to dictionary"""
        return {
            "timezone": entity.get("timezone", "UTC"),
        }
    
    @staticmethod
    def from_dict(data: dict, key: Optional[datastore.Key] = None) -> datastore.Entity:
        """Create Datastore entity from dictionary"""
        if key is None:
            key = datastore.Key(KIND_TIMEZONE, "default")
        
        entity = datastore.Entity(key=key)
        entity.update({
            "timezone": data["timezone"],
            "updated_at": datetime.utcnow(),
        })
        return entity

