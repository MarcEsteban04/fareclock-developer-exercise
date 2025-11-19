"""
Timezone API endpoints
"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import TimezoneSetting, ErrorResponse
from app.services.timezone_service import TimezoneService

router = APIRouter(prefix="/timezone")
timezone_service = TimezoneService()


@router.get("", response_model=TimezoneSetting)
async def get_timezone():
    """
    Get the current timezone setting.
    Returns UTC as default if not set.
    """
    try:
        timezone = timezone_service.get_timezone()
        return TimezoneSetting(timezone=timezone)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=TimezoneSetting)
async def set_timezone(setting: TimezoneSetting):
    """
    Set the timezone setting.
    This will be used for all shift datetime operations.
    """
    try:
        # Validate IANA timezone string (basic check)
        # In production, you might want more robust validation
        timezone = timezone_service.set_timezone(setting.timezone)
        return TimezoneSetting(timezone=timezone)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

