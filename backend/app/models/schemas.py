"""
Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TimezoneSetting(BaseModel):
    """Timezone setting schema"""
    timezone: str = Field(..., description="IANA timezone string")
    
    class Config:
        json_schema_extra = {
            "example": {
                "timezone": "America/New_York"
            }
        }


class WorkerBase(BaseModel):
    """Base worker schema"""
    name: str = Field(..., min_length=1, max_length=200, description="Worker name")


class WorkerCreate(WorkerBase):
    """Schema for creating a worker"""
    pass


class WorkerUpdate(BaseModel):
    """Schema for updating a worker"""
    name: str = Field(..., min_length=1, max_length=200, description="Worker name")


class Worker(WorkerBase):
    """Worker response schema"""
    id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ShiftBase(BaseModel):
    """Base shift schema"""
    worker_id: str = Field(..., description="ID of the associated worker")
    start: str = Field(..., description="Start datetime in ISO 8601 format")
    end: str = Field(..., description="End datetime in ISO 8601 format")


class ShiftCreate(ShiftBase):
    """Schema for creating a shift"""
    pass


class ShiftUpdate(BaseModel):
    """Schema for updating a shift"""
    worker_id: Optional[str] = Field(None, description="ID of the associated worker")
    start: Optional[str] = Field(None, description="Start datetime in ISO 8601 format")
    end: Optional[str] = Field(None, description="End datetime in ISO 8601 format")


class Shift(ShiftBase):
    """Shift response schema"""
    id: str
    duration: float = Field(..., description="Duration in hours (read-only, computed)")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ErrorResponse(BaseModel):
    """Error response schema"""
    message: str
    code: Optional[str] = None
    details: Optional[dict] = None

