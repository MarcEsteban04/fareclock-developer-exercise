"""
API v1 routes
"""

from fastapi import APIRouter
from app.api.v1 import timezone, workers, shifts

router = APIRouter()

# Include route modules
router.include_router(timezone.router, tags=["timezone"])
router.include_router(workers.router, prefix="/workers", tags=["workers"])
router.include_router(shifts.router, prefix="/shifts", tags=["shifts"])

