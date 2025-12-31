from datetime import datetime
from sqlalchemy import String, Text, Integer, BigInteger, ForeignKey, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column
from backend.core.database import Base


class Dataset(Base):
    __tablename__ = "datasets"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    version: Mapped[str] = mapped_column(String(50), nullable=False)
    storage_path: Mapped[str] = mapped_column(String(500), nullable=False)
    size_bytes: Mapped[int] = mapped_column(BigInteger, nullable=True)
    num_rows: Mapped[int] = mapped_column(Integer, nullable=True)
    num_features: Mapped[int] = mapped_column(Integer, nullable=True)
    schema: Mapped[dict] = mapped_column(JSON, nullable=True)
    metadata: Mapped[dict] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
