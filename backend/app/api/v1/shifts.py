"""
Shifts API endpoints
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.models.schemas import Shift, ShiftCreate, ShiftUpdate, ErrorResponse
from app.services.shift_service import ShiftService, ShiftValidationError
from app.services.timezone_service import TimezoneService
from app.utils.timezone import apply_timezone_to_shifts

router = APIRouter()
shift_service = ShiftService()
timezone_service = TimezoneService()


@router.get("", response_model=List[Shift])
async def get_shifts(worker_id: Optional[str] = Query(None, description="Filter by worker ID")):
    """Get all shifts, optionally filtered by worker_id. Times are returned in the configured timezone."""
    try:
        shifts = shift_service.get_shifts(worker_id=worker_id)
        # Apply timezone conversion
        timezone = timezone_service.get_timezone()
        shifts = apply_timezone_to_shifts(shifts, timezone)
        return shifts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{shift_id}", response_model=Shift)
async def get_shift(shift_id: str):
    """Get a shift by ID. Time is returned in the configured timezone."""
    try:
        shift = shift_service.get_shift(shift_id)
        if not shift:
            raise HTTPException(status_code=404, detail="Shift not found")
        # Apply timezone conversion
        timezone = timezone_service.get_timezone()
        [shift] = apply_timezone_to_shifts([shift], timezone)
        return shift
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=Shift, status_code=201)
async def create_shift(shift: ShiftCreate):
    """Create a new shift with validation"""
    try:
        created = shift_service.create_shift(
            worker_id=shift.worker_id,
            start=shift.start,
            end=shift.end
        )
        return created
    except ShiftValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{shift_id}", response_model=Shift)
async def update_shift(shift_id: str, shift: ShiftUpdate):
    """Update a shift with validation"""
    try:
        updated = shift_service.update_shift(
            shift_id=shift_id,
            worker_id=shift.worker_id,
            start=shift.start,
            end=shift.end
        )
        if not updated:
            raise HTTPException(status_code=404, detail="Shift not found")
        return updated
    except HTTPException:
        raise
    except ShiftValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{shift_id}", status_code=204)
async def delete_shift(shift_id: str):
    """Delete a shift"""
    try:
        deleted = shift_service.delete_shift(shift_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Shift not found")
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

