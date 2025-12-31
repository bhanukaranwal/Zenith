from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.core.database import get_db
from backend.core.security import get_current_active_user
from backend.models.user import User
from backend.models.dataset import Dataset
from backend.services.data import DataService

router = APIRouter()


@router.post("", status_code=201)
async def create_dataset(
    name: str,
    project_id: int,
    version: str,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    data_service = DataService(db)
    dataset = await data_service.create_dataset(
        name=name,
        project_id=project_id,
        version=version,
        file=file
    )
    return dataset


@router.get("")
async def list_datasets(
    project_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Dataset)
        .where(Dataset.project_id == project_id)
        .offset(skip)
        .limit(limit)
    )
    datasets = result.scalars().all()
    return datasets


@router.get("/{dataset_id}")
async def get_dataset(
    dataset_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Dataset).where(Dataset.id == dataset_id))
    dataset = result.scalar_one_or_none()
    
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    return dataset
