"""
Timezone conversion utilities
"""

from datetime import datetime
from typing import Optional

try:
    from zoneinfo import ZoneInfo
except ImportError:
    # Fallback for Python < 3.9
    from backports.zoneinfo import ZoneInfo

import pytz


def convert_to_timezone(iso_string: str, target_timezone: str) -> str:
    """
    Convert an ISO 8601 datetime string to the target timezone.
    Returns ISO 8601 string in the target timezone.
    """
    # Parse the ISO string (handles both with and without Z)
    if iso_string.endswith('Z'):
        dt = datetime.fromisoformat(iso_string.replace('Z', '+00:00'))
    else:
        dt = datetime.fromisoformat(iso_string)
    
    # If datetime is naive, assume it's UTC
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=ZoneInfo('UTC'))
    
    # Convert to target timezone
    try:
        target_tz = ZoneInfo(target_timezone)
    except Exception:
        # Fallback to pytz for older Python versions or unsupported timezones
        target_tz = pytz.timezone(target_timezone)
        dt = dt.astimezone(target_tz)
        return dt.isoformat()
    
    dt = dt.astimezone(target_tz)
    return dt.isoformat()


def apply_timezone_to_shifts(shifts: list, target_timezone: str) -> list:
    """
    Apply timezone conversion to a list of shifts.
    Updates start and end times to the target timezone.
    """
    converted_shifts = []
    for shift in shifts:
        shift_copy = shift.copy()
        if shift_copy.get("start"):
            shift_copy["start"] = convert_to_timezone(shift_copy["start"], target_timezone)
        if shift_copy.get("end"):
            shift_copy["end"] = convert_to_timezone(shift_copy["end"], target_timezone)
        converted_shifts.append(shift_copy)
    return converted_shifts

