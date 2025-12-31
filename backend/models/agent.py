from datetime import datetime
from sqlalchemy import String, Text, Integer, ForeignKey, DateTime, JSON, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from backend.core.database import Base
import enum


class AgentStatus(str, enum.Enum):
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class Agent(Base):
    __tablename__ = "agents"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    agent_type: Mapped[str] = mapped_column(String(100), nullable=False)
    config: Mapped[dict] = mapped_column(JSON, nullable=False)
    tools: Mapped[list] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class AgentExecution(Base):
    __tablename__ = "agent_executions"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    agent_id: Mapped[int] = mapped_column(ForeignKey("agents.id"), nullable=False)
    status: Mapped[AgentStatus] = mapped_column(SQLEnum(AgentStatus), default=AgentStatus.RUNNING, nullable=False)
    input_data: Mapped[dict] = mapped_column(JSON, nullable=False)
    output_data: Mapped[dict] = mapped_column(JSON, nullable=True)
    trace_id: Mapped[str] = mapped_column(String(255), nullable=True, index=True)
    start_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    metadata: Mapped[dict] = mapped_column(JSON, nullable=True)
