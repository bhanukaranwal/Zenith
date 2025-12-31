from datetime import datetime
from sqlalchemy import String, Text, Integer, ForeignKey, DateTime, JSON, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from backend.core.database import Base
import enum


class ModelStage(str, enum.Enum):
    STAGING = "staging"
    PRODUCTION = "production"
    ARCHIVED = "archived"


class DeploymentStatus(str, enum.Enum):
    PENDING = "pending"
    DEPLOYING = "deploying"
    RUNNING = "running"
    FAILED = "failed"
    STOPPED = "stopped"


class Model(Base):
    __tablename__ = "models"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class ModelVersion(Base):
    __tablename__ = "model_versions"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    model_id: Mapped[int] = mapped_column(ForeignKey("models.id"), nullable=False)
    version: Mapped[str] = mapped_column(String(50), nullable=False)
    run_id: Mapped[int] = mapped_column(ForeignKey("experiment_runs.id"), nullable=True)
    stage: Mapped[ModelStage] = mapped_column(SQLEnum(ModelStage), default=ModelStage.STAGING, nullable=False)
    storage_path: Mapped[str] = mapped_column(String(500), nullable=False)
    framework: Mapped[str] = mapped_column(String(100), nullable=True)
    metadata: Mapped[dict] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class Deployment(Base):
    __tablename__ = "deployments"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    model_version_id: Mapped[int] = mapped_column(ForeignKey("model_versions.id"), nullable=False)
    endpoint_url: Mapped[str] = mapped_column(String(500), nullable=True)
    status: Mapped[DeploymentStatus] = mapped_column(SQLEnum(DeploymentStatus), default=DeploymentStatus.PENDING, nullable=False)
    config: Mapped[dict] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
