"""
Shift service for CRUD operations with validation
"""

from google.cloud import datastore
from app.core.datastore import get_datastore_client, KIND_SHIFT
from app.models.entities import ShiftEntity, calculate_duration
from app.services.timezone_service import TimezoneService
from typing import List, Optional
from datetime import datetime
import uuid


class ShiftValidationError(Exception):
    """Custom exception for shift validation errors"""
    pass


class ShiftService:
    """Service for managing shifts with validation"""
    
    def __init__(self):
        self.client = get_datastore_client()
        self.timezone_service = TimezoneService()
    
    def _validate_shift(self, start_iso: str, end_iso: str, shift_id: Optional[str] = None) -> None:
        """
        Validate shift constraints:
        1. End time must be after start time
        2. Duration must not exceed 12 hours
        3. No overlapping shifts for the same worker
        """
        # Parse datetimes
        start = datetime.fromisoformat(start_iso.replace('Z', '+00:00'))
        end = datetime.fromisoformat(end_iso.replace('Z', '+00:00'))
        
        # Check end is after start
        if end <= start:
            raise ShiftValidationError("End time must be after start time")
        
        # Check duration doesn't exceed 12 hours
        duration = calculate_duration(start_iso, end_iso)
        if duration > 12.0:
            raise ShiftValidationError(f"Shift duration ({duration:.2f} hours) exceeds maximum of 12 hours")
        
        # Note: Overlap checking is done in create/update methods with worker_id
    
    def _check_overlaps(self, worker_id: str, start_iso: str, end_iso: str, exclude_shift_id: Optional[str] = None) -> None:
        """
        Check if a shift overlaps with existing shifts for the same worker.
        Raises ShiftValidationError if overlap is found.
        """
        start = datetime.fromisoformat(start_iso.replace('Z', '+00:00'))
        end = datetime.fromisoformat(end_iso.replace('Z', '+00:00'))
        
        # Query all shifts for this worker
        query = self.client.query(kind=KIND_SHIFT)
        query.add_filter("worker_id", "=", worker_id)
        
        for entity in query.fetch():
            # Skip the shift we're updating
            if exclude_shift_id and entity.key.id_or_name == exclude_shift_id:
                continue
            
            existing_start = datetime.fromisoformat(entity.get("start").replace('Z', '+00:00'))
            existing_end = datetime.fromisoformat(entity.get("end").replace('Z', '+00:00'))
            
            # Check for overlap: two time ranges overlap if:
            # start1 < end2 AND start2 < end1
            if start < existing_end and existing_start < end:
                raise ShiftValidationError(
                    f"Shift overlaps with existing shift "
                    f"({existing_start.isoformat()} to {existing_end.isoformat()})"
                )
    
    def create_shift(self, worker_id: str, start: str, end: str) -> dict:
        """Create a new shift with validation"""
        # Validate shift
        self._validate_shift(start, end)
        
        # Check for overlaps
        self._check_overlaps(worker_id, start, end)
        
        # Create shift
        shift_id = str(uuid.uuid4())
        key = self.client.key(KIND_SHIFT, shift_id)
        
        entity = ShiftEntity.from_dict({
            "id": shift_id,
            "worker_id": worker_id,
            "start": start,
            "end": end,
        }, key)
        
        self.client.put(entity)
        return ShiftEntity.to_dict(entity)
    
    def get_shift(self, shift_id: str) -> Optional[dict]:
        """Get a shift by ID"""
        key = self.client.key(KIND_SHIFT, shift_id)
        entity = self.client.get(key)
        
        if entity:
            return ShiftEntity.to_dict(entity)
        return None
    
    def get_shifts(self, worker_id: Optional[str] = None) -> List[dict]:
        """Get all shifts, optionally filtered by worker_id"""
        query = self.client.query(kind=KIND_SHIFT)
        
        if worker_id:
            query.add_filter("worker_id", "=", worker_id)
        
        query.order = ["start"]
        
        entities = list(query.fetch())
        return [ShiftEntity.to_dict(entity) for entity in entities]
    
    def update_shift(self, shift_id: str, worker_id: Optional[str] = None, 
                     start: Optional[str] = None, end: Optional[str] = None) -> Optional[dict]:
        """Update a shift with validation"""
        key = self.client.key(KIND_SHIFT, shift_id)
        entity = self.client.get(key)
        
        if not entity:
            return None
        
        # Get current values
        current_worker_id = worker_id if worker_id is not None else entity.get("worker_id")
        current_start = start if start is not None else entity.get("start")
        current_end = end if end is not None else entity.get("end")
        
        # Validate shift
        self._validate_shift(current_start, current_end, shift_id)
        
        # Check for overlaps (excluding current shift)
        self._check_overlaps(current_worker_id, current_start, current_end, exclude_shift_id=shift_id)
        
        # Update entity
        if worker_id is not None:
            entity["worker_id"] = worker_id
        if start is not None:
            entity["start"] = start
        if end is not None:
            entity["end"] = end
        
        entity["updated_at"] = datetime.utcnow()
        
        self.client.put(entity)
        return ShiftEntity.to_dict(entity)
    
    def delete_shift(self, shift_id: str) -> bool:
        """Delete a shift"""
        key = self.client.key(KIND_SHIFT, shift_id)
        entity = self.client.get(key)
        
        if not entity:
            return False
        
        self.client.delete(key)
        return True

