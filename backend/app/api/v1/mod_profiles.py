from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.models.mod_profile import ModProfileCreate, ModProfileResponse
from app.core.database import get_db
from app.services.mod_profile_service import ModProfileService

router = APIRouter(prefix="/mod-profiles", tags=["mod-profiles"])


@router.post("/", response_model=ModProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_mod_profile(mod_profile: ModProfileCreate, db: AsyncSession = Depends(get_db)):
    service = ModProfileService(db)
    return await service.create(mod_profile)


@router.get("/", response_model=List[ModProfileResponse])
async def list_mod_profiles(
    game_version: str = Query(None, description="Filter by game version"),
    loader: str = Query(None, description="Filter by loader type"),
    db: AsyncSession = Depends(get_db),
):
    service = ModProfileService(db)
    return await service.list(game_version=game_version, loader=loader)


@router.get("/{mod_profile_id}", response_model=ModProfileResponse)
async def get_mod_profile(mod_profile_id: str, db: AsyncSession = Depends(get_db)):
    service = ModProfileService(db)
    mod_profile = await service.get(mod_profile_id)
    if not mod_profile:
        raise HTTPException(status_code=404, detail="Mod profile not found")
    return mod_profile


@router.patch("/{mod_profile_id}", response_model=ModProfileResponse)
async def update_mod_profile(mod_profile_id: str, mod_profile: ModProfileCreate, db: AsyncSession = Depends(get_db)):
    service = ModProfileService(db)
    updated = await service.update(mod_profile_id, mod_profile)
    if not updated:
        raise HTTPException(status_code=404, detail="Mod profile not found")
    return updated


@router.delete("/{mod_profile_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_mod_profile(mod_profile_id: str, db: AsyncSession = Depends(get_db)):
    service = ModProfileService(db)
    deleted = await service.delete(mod_profile_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Mod profile not found")
    return
