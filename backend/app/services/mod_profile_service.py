from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func
from typing import Optional, List
from datetime import datetime
import uuid

from app.models.mod_profile_db import ModProfileModel
from app.models.mod_profile import ModProfileCreate, ModProfileResponse


class ModProfileService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, mod_profile: ModProfileCreate) -> ModProfileResponse:
        db_instance = ModProfileModel(
            id=str(uuid.uuid4()),
            name=mod_profile.name,
            description=mod_profile.description,
            game_version=mod_profile.game_version,
            loader=mod_profile.loader,
            loader_version=mod_profile.loader_version,
            mcversion=mod_profile.mcversion,
            jar_url=mod_profile.jar_url,
            checksum=mod_profile.checksum,
        )
        self.db.add(db_instance)
        await self.db.commit()
        await self.db.refresh(db_instance)
        return ModProfileResponse.model_validate(db_instance)

    async def get(self, mod_profile_id: str) -> Optional[ModProfileResponse]:
        result = await self.db.execute(select(ModProfileModel).where(ModProfileModel.id == mod_profile_id))
        row = result.scalar_one_or_none()
        if not row:
            return None
        return ModProfileResponse.model_validate(row)

    async def list(self, game_version: str = None, loader: str = None) -> List[ModProfileResponse]:
        query = select(ModProfileModel)
        if game_version:
            query = query.where(ModProfileModel.game_version == game_version)
        if loader:
            query = query.where(ModProfileModel.loader == loader)
        query = query.order_by(ModProfileModel.created_at.desc())
        result = await self.db.execute(query)
        rows = result.scalars().all()
        return [ModProfileResponse.model_validate(row) for row in rows]

    async def update(self, mod_profile_id: str, mod_profile: ModProfileCreate) -> Optional[ModProfileResponse]:
        result = await self.db.execute(select(ModProfileModel).where(ModProfileModel.id == mod_profile_id))
        db_instance = result.scalar_one_or_none()
        if not db_instance:
            return None
        db_instance.name = mod_profile.name
        db_instance.description = mod_profile.description
        db_instance.game_version = mod_profile.game_version
        db_instance.loader = mod_profile.loader
        db_instance.loader_version = mod_profile.loader_version
        db_instance.mcversion = mod_profile.mcversion
        db_instance.jar_url = mod_profile.jar_url
        db_instance.checksum = mod_profile.checksum
        db_instance.updated_at = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(db_instance)
        return ModProfileResponse.model_validate(db_instance)

    async def delete(self, mod_profile_id: str) -> bool:
        result = await self.db.execute(select(ModProfileModel).where(ModProfileModel.id == mod_profile_id))
        db_instance = result.scalar_one_or_none()
        if not db_instance:
            return False
        await self.db.delete(db_instance)
        await self.db.commit()
        return True
