from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.core.database import get_db
from backend.core.security import get_current_active_user
from backend.models.user import User
from backend.models.feature import FeatureGroup, Feature
from backend.services.data import FeatureStoreService

router = APIRouter()


@router.post("/groups", status_code=201)
async def create_feature_group(
    name: str,
    project_id: int,
    entity_columns: List[str],
    description: str = None,
    online_enabled: bool = True,
    offline_enabled: bool = True,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    feature_group = FeatureGroup(
        name=name,
        description=description,
        project_id=project_id,
        online_enabled=online_enabled,
        offline_enabled=offline_enabled,
        entity_columns=entity_columns
    )
    
    db.add(feature_group)
    await db.commit()
    await db.refresh(feature_group)
    
    return feature_group


@router.post("/groups/{group_id}/features", status_code=201)
async def add_feature(
    group_id: int,
    name: str,
    dtype: str,
    description: str = None,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    feature = Feature(
        name=name,
        description=description,
        feature_group_id=group_id,
        dtype=dtype
    )
    
    db.add(feature)
    await db.commit()
    await db.refresh(feature)
    
    return feature


@router.post("/groups/{group_id}/ingest")
async def ingest_features(
    group_id: int,
    features: Dict[str, Any],
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    feature_service = FeatureStoreService(db)
    await feature_service.ingest_features(group_id, features)
    return {"status": "success", "message": "Features ingested"}


@router.get("/groups/{group_id}/features")
async def get_online_features(
    group_id: int,
    entity_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    feature_service = FeatureStoreService(db)
    features = await feature_service.get_online_features(group_id, entity_id)
    return features
