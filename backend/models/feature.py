from datetime import datetime
from sqlalchemy import String, Text, Integer, ForeignKey, DateTime, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from backend.core.database import Base


class FeatureGroup(Base):
    __tablename__ = "feature_groups"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    online_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    offline_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    entity_columns: Mapped[list] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class Feature(Base):
    __tablename__ = "features"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    feature_group_id: Mapped[int] = mapped_column(ForeignKey("feature_groups.id"), nullable=False)
    dtype: Mapped[str] = mapped_column(String(50), nullable=False)
    transformation: Mapped[dict] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
