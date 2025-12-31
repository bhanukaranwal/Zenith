from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any, List
from backend.models.experiment import RunStatus


class ExperimentCreate(BaseModel):
    name: str
    description: Optional[str] = None
    project_id: int


class ExperimentResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    project_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class RunCreate(BaseModel):
    experiment_id: int
    run_name: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    tags: Optional[Dict[str, str]] = None


class RunUpdate(BaseModel):
    status: Optional[RunStatus] = None
    metadata: Optional[Dict[str, Any]] = None


class RunResponse(BaseModel):
    id: int
    experiment_id: int
    run_name: Optional[str]
    status: RunStatus
    start_time: datetime
    end_time: Optional[datetime]
    artifact_uri: Optional[str]
    
    class Config:
        from_attributes = True


class MetricLog(BaseModel):
    key: str
    value: float
    step: Optional[int] = 0


class ParameterLog(BaseModel):
    key: str
    value: str


class MetricResponse(BaseModel):
    id: int
    run_id: int
    key: str
    value: float
    timestamp: datetime
    step: int
    
    class Config:
        from_attributes = True
