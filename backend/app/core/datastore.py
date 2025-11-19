"""
Google Cloud Datastore client and utilities
"""

from google.cloud import datastore
from app.core.config import settings
import os


def get_datastore_client() -> datastore.Client:
    """
    Get a Datastore client instance.
    Uses emulator if DATASTORE_EMULATOR_HOST is set, otherwise uses GCP.
    """
    if settings.DATASTORE_EMULATOR_HOST:
        # Use emulator for local development
        os.environ["DATASTORE_EMULATOR_HOST"] = settings.DATASTORE_EMULATOR_HOST
        client = datastore.Client(project=settings.GCP_PROJECT_ID)
    else:
        # Use real GCP Datastore
        client = datastore.Client(project=settings.GCP_PROJECT_ID)
    
    return client


# Entity kind constants
KIND_TIMEZONE = "Timezone"
KIND_WORKER = "Worker"
KIND_SHIFT = "Shift"

