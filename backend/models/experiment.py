from datetime import datetime
from sqlalchemy import String, Text, Integer, Float, ForeignKey, DateTime, JSON, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.core.database import Base
import enum


class RunStatus(str, enum.Enum):
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    STOPPED = "stopped"


class Experiment(Base):
    __tablename__ = "experiments"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class ExperimentRun(Base):
    __tablename__ = "experiment_runs"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    experiment_id: Mapped[int] = mapped_column(ForeignKey("experiments.id"), nullable=False)
    run_name: Mapped[str] = mapped_column(String(255), nullable=True)
    status: Mapped[RunStatus] = mapped_column(SQLEnum(RunStatus), default=RunStatus.RUNNING, nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    artifact_uri: Mapped[str] = mapped_column(String(500), nullable=True)
    metadata: Mapped[dict] = mapped_column(JSON, nullable=True)
    tags: Mapped[dict] = mapped_column(JSON, nullable=True)


class Parameter(Base):
    __tablename__ = "parameters"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    run_id: Mapped[int] = mapped_column(ForeignKey("experiment_runs.id"), nullable=False)
    key: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    value: Mapped[str] = mapped_column(Text, nullable=False)


class Metric(Base):
    __tablename__ = "metrics"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    run_id: Mapped[int] = mapped_column(ForeignKey("experiment_runs.id"), nullable=False)
    key: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    step: Mapped[int] = mapped_column(Integer, default=0, nullable=True)
