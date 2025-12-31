from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.core.database import get_db
from backend.core.security import get_current_active_user
from backend.models.user import User
from backend.models.model import Deployment
from backend.schemas.model import DeploymentCreate, DeploymentResponse
from backend.services.inference import InferenceService

router = APIRouter()


@router.post("", response_model=DeploymentResponse, status_code=status.HTTP_201_CREATED)
async def create_deployment(
    deployment_data: DeploymentCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    deployment = Deployment(
        name=deployment_data.name,
        model_version_id=deployment_data.model_version_id,
        config=deployment_data.config
    )
    
    db.add(deployment)
    await db.commit()
    await db.refresh(deployment)
    
    inference_service = InferenceService(db)
    endpoint = await inference_service.deploy_model(deployment.id)
    
    deployment.endpoint_url = endpoint
    deployment.status = "running"
    await db.commit()
    
    return deployment


@router.get("", response_model=List[DeploymentResponse])
async def list_deployments(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Deployment).offset(skip).limit(limit)
    )
    deployments = result.scalars().all()
    return deployments


@router.get("/{deployment_id}", response_model=DeploymentResponse)
async def get_deployment(
    deployment_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Deployment).where(Deployment.id == deployment_id))
    deployment = result.scalar_one_or_none()
    
    if not deployment:
        raise HTTPException(status_code=404, detail="Deployment not found")
    
    return deployment


@router.post("/{deployment_id}/predict")
async def predict(
    deployment_id: int,
    inputs: dict,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    inference_service = InferenceService(db)
    predictions = await inference_service.predict(deployment_id, inputs)
    return predictions


@router.delete("/{deployment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_deployment(
    deployment_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Deployment).where(Deployment.id == deployment_id))
    deployment = result.scalar_one_or_none()
    
    if not deployment:
        raise HTTPException(status_code=404, detail="Deployment not found")
    
    await db.delete(deployment)
    await db.commit()
    
    return None
