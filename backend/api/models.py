from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.core.database import get_db
from backend.core.security import get_current_active_user
from backend.models.user import User
from backend.models.model import Model, ModelVersion
from backend.schemas.model import (
    ModelCreate, ModelResponse,
    ModelVersionCreate, ModelVersionResponse
)

router = APIRouter()


@router.post("", response_model=ModelResponse, status_code=status.HTTP_201_CREATED)
async def create_model(
    model_data: ModelCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    model = Model(
        name=model_data.name,
        description=model_data.description,
        project_id=model_data.project_id
    )
    
    db.add(model)
    await db.commit()
    await db.refresh(model)
    
    return model


@router.get("", response_model=List[ModelResponse])
async def list_models(
    project_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Model)
        .where(Model.project_id == project_id)
        .offset(skip)
        .limit(limit)
    )
    models = result.scalars().all()
    return models


@router.post("/versions", response_model=ModelVersionResponse, status_code=status.HTTP_201_CREATED)
async def create_model_version(
    version_data: ModelVersionCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    version = ModelVersion(
        model_id=version_data.model_id,
        version=version_data.version,
        run_id=version_data.run_id,
        storage_path=version_data.storage_path,
        framework=version_data.framework,
        metadata=version_data.metadata
    )
    
    db.add(version)
    await db.commit()
    await db.refresh(version)
    
    return version


@router.get("/{model_id}/versions", response_model=List[ModelVersionResponse])
async def list_model_versions(
    model_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(ModelVersion).where(ModelVersion.model_id == model_id)
    )
    versions = result.scalars().all()
    return versions


@router.post("/versions/{version_id}/promote")
async def promote_model_version(
    version_id: int,
    stage: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(ModelVersion).where(ModelVersion.id == version_id))
    version = result.scalar_one_or_none()
    
    if not version:
        raise HTTPException(status_code=404, detail="Model version not found")
    
    version.stage = stage
    await db.commit()
    
    return {"status": "success", "message": f"Model promoted to {stage}"}
