from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database import get_db
from backend.core.security import get_current_active_user
from backend.models.user import User
from backend.services.monitoring import MonitoringService

router = APIRouter()


@router.get("/deployments/{deployment_id}/metrics")
async def get_deployment_metrics(
    deployment_id: int,
    start_time: str = None,
    end_time: str = None,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    monitoring_service = MonitoringService(db)
    metrics = await monitoring_service.get_deployment_metrics(
        deployment_id, start_time, end_time
    )
    return metrics


@router.post("/deployments/{deployment_id}/drift")
async def check_drift(
    deployment_id: int,
    reference_data: Dict[str, Any],
    current_data: Dict[str, Any],
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    monitoring_service = MonitoringService(db)
    drift_report = await monitoring_service.detect_drift(
        deployment_id, reference_data, current_data
    )
    return drift_report


@router.get("/deployments/{deployment_id}/traces")
async def get_traces(
    deployment_id: int,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    monitoring_service = MonitoringService(db)
    traces = await monitoring_service.get_traces(deployment_id, limit)
    return traces
