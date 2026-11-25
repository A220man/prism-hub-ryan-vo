import uuid
from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.dialects.sqlite import JSON
from app.core.database import Base
from datetime import datetime


class ModProfileModel(Base):
    __tablename__ = "mod_profiles"

    id = Column(String(36), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    game_version = Column(String(50), nullable=False)
    loader = Column(String(50), nullable=False)
    loader_version = Column(String(50), nullable=True)
    mcversion = Column(String(20), nullable=True)
    jar_url = Column(String(500), nullable=True)
    checksum = Column(String(64), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
