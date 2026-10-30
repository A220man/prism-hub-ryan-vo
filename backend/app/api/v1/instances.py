from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List
import uuid
from datetime import datetime

from app.models.instance import (
    InstanceCreate,
    InstanceUpdate,
    InstanceResponse,
    InstanceListResponse,
    InstanceStatus,
)
from app.core.database import get_db
from app.services.instance_service import InstanceService

router = APIRouter()


@router.post("/instances", response_model=InstanceResponse, status_code=status.HTTP_201_CREATED)
async def create_instance(instance: InstanceCreate, db: AsyncSession = Depends(get_db)):
    service = InstanceService(db)
    return await service.create(instance)


@router.get("/instances", response_model=InstanceListResponse)
async def list_instances(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: InstanceStatus | None = None,
    db: AsyncSession = Depends(get_db),
):
    service = InstanceService(db)
    return await service.list(page=page, page_size=page_size, status_filter=status)


@router.get("/instances/{instance_id}", response_model=InstanceResponse)
async def get_instance(instance_id: str, db: AsyncSession = Depends(get_db)):
    service = InstanceService(db)
    instance = await service.get(instance_id)
    if not instance:
        raise HTTPException(status_code=404, detail="Instance not found")
    return instance


@router.patch("/instances/{instance_id}", response_model=InstanceResponse)
async def update_instance(instance_id: str, instance: InstanceUpdate, db: AsyncSession = Depends(get_db)):
    service = InstanceService(db)
    updated = await service.update(instance_id, instance)
    if not updated:
        raise HTTPException(status_code=404, detail="Instance not found")
    return updated


@router.delete("/instances/{instance_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_instance(instance_id: str, db: AsyncSession = Depends(get_db)):
    service = InstanceService(db)
    deleted = await service.delete(instance_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Instance not found")


@router.post("/instances/{instance_id}/launch", response_model=InstanceResponse)
async def launch_instance(instance_id: str, db: AsyncSession = Depends(get_db)):
    service = InstanceService(db)
    instance = await service.launch(instance_id)
    if not instance:
        raise HTTPException(status_code=404, detail="Instance not found")
    return instance
@router.get("/instances/{instance_id}/launch-info")
async def get_launch_info(instance_id: str, db: AsyncSession = Depends(get_db)):
    service = InstanceService(db)
    launch_info = await service.get_launch_info(instance_id)
    if not launch_info:
        raise HTTPException(status_code=404, detail="Instance not found")
    return launch_info