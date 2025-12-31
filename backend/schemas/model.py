from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any
from backend.models.model import ModelStage, DeploymentStatus


class ModelCreate(BaseModel):
    name: str
    description: Optional[str] = None
    project_id: int


class ModelResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    project_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class ModelVersionCreate(BaseModel):
    model_id: int
    version: str
    run_id: Optional[int] = None
    storage_path: str
    framework: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class ModelVersionResponse(BaseModel):
    id: int
    model_id: int
    version: str
    stage: ModelStage
    storage_path: str
    framework: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class DeploymentCreate(BaseModel):
    name: str
    model_version_id: int
    config: Optional[Dict[str, Any]] = None


class DeploymentResponse(BaseModel):
    id: int
    name: str
    model_version_id: int
    endpoint_url: Optional[str]
    status: DeploymentStatus
    created_at: datetime
    
    class Config:
        from_attributes = True
