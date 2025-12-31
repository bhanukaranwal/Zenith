from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.core.database import get_db
from backend.core.security import get_current_active_user
from backend.models.user import User
from backend.models.experiment import Experiment, ExperimentRun, Metric, Parameter
from backend.schemas.experiment import (
    ExperimentCreate, ExperimentResponse,
    RunCreate, RunResponse, RunUpdate,
    MetricLog, ParameterLog, MetricResponse
)

router = APIRouter()


@router.post("", response_model=ExperimentResponse, status_code=status.HTTP_201_CREATED)
async def create_experiment(
    experiment_data: ExperimentCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    experiment = Experiment(
        name=experiment_data.name,
        description=experiment_data.description,
        project_id=experiment_data.project_id
    )
    
    db.add(experiment)
    await db.commit()
    await db.refresh(experiment)
    
    return experiment


@router.get("", response_model=List[ExperimentResponse])
async def list_experiments(
    project_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Experiment)
        .where(Experiment.project_id == project_id)
        .offset(skip)
        .limit(limit)
    )
    experiments = result.scalars().all()
    return experiments


@router.post("/runs", response_model=RunResponse, status_code=status.HTTP_201_CREATED)
async def create_run(
    run_data: RunCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    run = ExperimentRun(
        experiment_id=run_data.experiment_id,
        run_name=run_data.run_name,
        metadata=run_data.metadata,
        tags=run_data.tags
    )
    
    db.add(run)
    await db.commit()
    await db.refresh(run)
    
    return run


@router.post("/runs/{run_id}/metrics", status_code=status.HTTP_201_CREATED)
async def log_metrics(
    run_id: int,
    metrics: List[MetricLog],
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    metric_objects = [
        Metric(run_id=run_id, key=m.key, value=m.value, step=m.step)
        for m in metrics
    ]
    
    db.add_all(metric_objects)
    await db.commit()
    
    return {"status": "success", "count": len(metrics)}


@router.post("/runs/{run_id}/parameters", status_code=status.HTTP_201_CREATED)
async def log_parameters(
    run_id: int,
    parameters: List[ParameterLog],
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    param_objects = [
        Parameter(run_id=run_id, key=p.key, value=p.value)
        for p in parameters
    ]
    
    db.add_all(param_objects)
    await db.commit()
    
    return {"status": "success", "count": len(parameters)}


@router.get("/runs/{run_id}", response_model=RunResponse)
async def get_run(
    run_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(ExperimentRun).where(ExperimentRun.id == run_id))
    run = result.scalar_one_or_none()
    
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    
    return run


@router.get("/runs/{run_id}/metrics", response_model=List[MetricResponse])
async def get_run_metrics(
    run_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Metric).where(Metric.run_id == run_id))
    metrics = result.scalars().all()
    return metrics


@router.put("/runs/{run_id}", response_model=RunResponse)
async def update_run(
    run_id: int,
    run_data: RunUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(ExperimentRun).where(ExperimentRun.id == run_id))
    run = result.scalar_one_or_none()
    
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    
    if run_data.status:
        run.status = run_data.status
    if run_data.metadata:
        run.metadata = run_data.metadata
    
    await db.commit()
    await db.refresh(run)
    
    return run
