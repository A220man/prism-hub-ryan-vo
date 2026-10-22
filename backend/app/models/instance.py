from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class InstanceStatus(str, Enum):
    CREATED = "created"
    DOWNLOADING = "downloading"
    READY = "ready"
    LAUNCHING = "launching"
    RUNNING = "running"
    ERROR = "error"


class InstanceBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    version: str = Field(..., min_length=1, max_length=50)
    loader: Optional[str] = Field(None, max_length=50)
    loader_version: Optional[str] = Field(None, max_length=50)
    java_version: Optional[str] = Field(None, max_length=20)
    memory_min: int = Field(512, ge=256, le=16384)
    memory_max: int = Field(2048, ge=512, le=32768)
    game_dir: Optional[str] = None
    resolution_width: int = Field(854, ge=320, le=7680)
    resolution_height: int = Field(480, ge=240, le=4320)
    fullscreen: bool = False


class InstanceCreate(InstanceBase):
    pass


class InstanceUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    version: Optional[str] = Field(None, min_length=1, max_length=50)
    loader: Optional[str] = Field(None, max_length=50)
    loader_version: Optional[str] = Field(None, max_length=50)
    java_version: Optional[str] = Field(None, max_length=20)
    memory_min: Optional[int] = Field(None, ge=256, le=16384)
    memory_max: Optional[int] = Field(None, ge=512, le=32768)
    game_dir: Optional[str] = None
    resolution_width: Optional[int] = Field(None, ge=320, le=7680)
    resolution_height: Optional[int] = Field(None, ge=240, le=4320)
    fullscreen: Optional[bool] = None


class InstanceResponse(InstanceBase):
    id: str
    status: InstanceStatus
    created_at: datetime
    updated_at: datetime
    last_played: Optional[datetime] = None
    play_time_seconds: int = 0

    class Config:
        from_attributes = True


class InstanceListResponse(BaseModel):
    instances: List[InstanceResponse]
    total: int
    page: int
    page_size: int