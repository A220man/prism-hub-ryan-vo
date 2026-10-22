from sqlalchemy import Column, String, Integer, DateTime, Enum as SQLEnum, Text
from sqlalchemy.dialects.sqlite import JSON
from app.core.database import Base
from app.models.instance import InstanceStatus
from datetime import datetime
import uuid


class InstanceModel(Base):
    __tablename__ = "instances"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    version = Column(String(50), nullable=False)
    loader = Column(String(50), nullable=True)
    loader_version = Column(String(50), nullable=True)
    java_version = Column(String(20), nullable=True)
    memory_min = Column(Integer, default=512)
    memory_max = Column(Integer, default=2048)
    game_dir = Column(Text, nullable=True)
    resolution_width = Column(Integer, default=854)
    resolution_height = Column(Integer, default=480)
    fullscreen = Column(Integer, default=0)
    status = Column(SQLEnum(InstanceStatus), default=InstanceStatus.CREATED, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_played = Column(DateTime, nullable=True)
    play_time_seconds = Column(Integer, default=0)