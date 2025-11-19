"""
Timezone service for managing timezone settings
"""

from google.cloud import datastore
from app.core.datastore import get_datastore_client, KIND_TIMEZONE
from app.models.entities import TimezoneEntity
from typing import Optional


class TimezoneService:
    """Service for managing timezone settings"""
    
    def __init__(self):
        self.client = get_datastore_client()
        self.default_key = self.client.key(KIND_TIMEZONE, "default")
    
    def get_timezone(self) -> Optional[str]:
        """
        Get the current timezone setting.
        Returns UTC as default if not set.
        """
        try:
            entity = self.client.get(self.default_key)
            if entity:
                return TimezoneEntity.to_dict(entity).get("timezone", "UTC")
            return "UTC"
        except Exception:
            return "UTC"
    
    def set_timezone(self, timezone: str) -> str:
        """
        Set the timezone setting.
        Returns the set timezone.
        """
        entity = TimezoneEntity.from_dict({"timezone": timezone}, self.default_key)
        self.client.put(entity)
        return timezone

