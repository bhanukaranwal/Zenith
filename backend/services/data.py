from typing import Dict, Any, Optional
import aiofiles
import json
import pandas as pd
import pyarrow.parquet as pq
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import UploadFile
import redis.asyncio as aioredis

from backend.models.dataset import Dataset
from backend.models.feature import FeatureGroup
from backend.core.config import settings


class DataService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.storage_path = Path("/app/artifacts/datasets")
        self.storage_path.mkdir(parents=True, exist_ok=True)
    
    async def create_dataset(
        self,
        name: str,
        project_id: int,
        version: str,
        file: UploadFile
    ) -> Dataset:
        file_path = self.storage_path / f"{name}_{version}.parquet"
        
        content = await file.read()
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(content)
        
        df = pd.read_csv(pd.io.common.BytesIO(content)) if file.filename.endswith('.csv') else pd.read_parquet(pd.io.common.BytesIO(content))
        
        dataset = Dataset(
            name=name,
            project_id=project_id,
            version=version,
            storage_path=str(file_path),
            size_bytes=len(content),
            num_rows=len(df),
            num_features=len(df.columns),
            schema={col: str(dtype) for col, dtype in df.dtypes.items()},
            metadata={"columns": list(df.columns)}
        )
        
        self.db.add(dataset)
        await self.db.commit()
        await self.db.refresh(dataset)
        
        return dataset
    
    async def get_dataset_stats(self, dataset_id: int) -> Dict[str, Any]:
        result = await self.db.execute(select(Dataset).where(Dataset.id == dataset_id))
        dataset = result.scalar_one_or_none()
        
        if not dataset:
            return {}
        
        df = pd.read_parquet(dataset.storage_path)
        
        return {
            "num_rows": len(df),
            "num_columns": len(df.columns),
            "memory_usage": df.memory_usage(deep=True).sum(),
            "column_types": df.dtypes.to_dict(),
            "missing_values": df.isnull().sum().to_dict(),
            "numeric_summary": df.describe().to_dict()
        }


class FeatureStoreService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.redis_client = aioredis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True
        )
        self.offline_path = Path("/app/artifacts/features")
        self.offline_path.mkdir(parents=True, exist_ok=True)
    
    async def ingest_features(
        self,
        group_id: int,
        features: Dict[str, Any]
    ):
        result = await self.db.execute(select(FeatureGroup).where(FeatureGroup.id == group_id))
        group = result.scalar_one_or_none()
        
        if not group:
            raise ValueError("Feature group not found")
        
        if group.online_enabled:
            entity_key = features.get(group.entity_columns[0])
            redis_key = f"features:{group.name}:{entity_key}"
            await self.redis_client.setex(
                redis_key,
                settings.FEATURE_STORE_ONLINE_TTL,
                json.dumps(features)
            )
        
        if group.offline_enabled:
            offline_file = self.offline_path / f"{group.name}.parquet"
            df = pd.DataFrame([features])
            
            if offline_file.exists():
                existing_df = pd.read_parquet(offline_file)
                df = pd.concat([existing_df, df], ignore_index=True)
            
            df.to_parquet(offline_file, index=False)
    
    async def get_online_features(
        self,
        group_id: int,
        entity_id: str
    ) -> Optional[Dict[str, Any]]:
        result = await self.db.execute(select(FeatureGroup).where(FeatureGroup.id == group_id))
        group = result.scalar_one_or_none()
        
        if not group:
            return None
        
        redis_key = f"features:{group.name}:{entity_id}"
        features_json = await self.redis_client.get(redis_key)
        
        if features_json:
            return json.loads(features_json)
        
        return None
    
    async def get_offline_features(
        self,
        group_id: int,
        entity_ids: list,
        feature_names: list = None
    ) -> pd.DataFrame:
        result = await self.db.execute(select(FeatureGroup).where(FeatureGroup.id == group_id))
        group = result.scalar_one_or_none()
        
        if not group:
            return pd.DataFrame()
        
        offline_file = self.offline_path / f"{group.name}.parquet"
        
        if not offline_file.exists():
            return pd.DataFrame()
        
        df = pd.read_parquet(offline_file)
        entity_col = group.entity_columns[0]
        df = df[df[entity_col].isin(entity_ids)]
        
        if feature_names:
            cols = [entity_col] + feature_names
            df = df[cols]
        
        return df
