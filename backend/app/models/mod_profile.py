from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ModProfileBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    game_version: str = Field(..., min_length=1, max_length=50)
    loader: str = Field(..., max_length=50)
    loader_version: Optional[str] = Field(None, max_length=50)
    mcversion: Optional[str] = Field(None, max_length=20)
    jar_url: Optional[str] = Field(None, max_length=500)
    checksum: Optional[str] = Field(None, max_length=64)


class ModProfileCreate(ModProfileBase):
    pass


class ModProfileResponse(ModProfileBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
