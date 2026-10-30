from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func
from typing import List, Optional
from datetime import datetime

from app.models.instance_db import InstanceModel
from app.models.instance import InstanceCreate, InstanceUpdate, InstanceResponse, InstanceListResponse, InstanceStatus
from app.services.java_detection import java_detection_service, JavaInfo


class InstanceService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, instance: InstanceCreate) -> InstanceResponse:
        db_instance = InstanceModel(
            name=instance.name,
            version=instance.version,
            loader=instance.loader,
            loader_version=instance.loader_version,
            java_version=instance.java_version,
            memory_min=instance.memory_min,
            memory_max=instance.memory_max,
            game_dir=instance.game_dir,
            resolution_width=instance.resolution_width,
            resolution_height=instance.resolution_height,
            fullscreen=1 if instance.fullscreen else 0,
            status=InstanceStatus.CREATED,
        )
        self.db.add(db_instance)
        await self.db.commit()
        await self.db.refresh(db_instance)
        return InstanceResponse.model_validate(db_instance)

    async def list(
        self,
        page: int = 1,
        page_size: int = 20,
        status_filter: Optional[InstanceStatus] = None,
    ) -> InstanceListResponse:
        query = select(InstanceModel)
        if status_filter:
            query = query.where(InstanceModel.status == status_filter)

        total_query = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(total_query)).scalar()

        query = query.order_by(InstanceModel.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(query)
        instances = [InstanceResponse.model_validate(row) for row in result.scalars().all()]

        return InstanceListResponse(instances=instances, total=total, page=page, page_size=page_size)

    async def get(self, instance_id: str) -> Optional[InstanceResponse]:
        result = await self.db.execute(select(InstanceModel).where(InstanceModel.id == instance_id))
        instance = result.scalar_one_or_none()
        if instance:
            return InstanceResponse.model_validate(instance)
        return None

    async def update(self, instance_id: str, instance: InstanceUpdate) -> Optional[InstanceResponse]:
        result = await self.db.execute(select(InstanceModel).where(InstanceModel.id == instance_id))
        db_instance = result.scalar_one_or_none()
        if not db_instance:
            return None

        update_data = instance.model_dump(exclude_unset=True)
        if "fullscreen" in update_data:
            update_data["fullscreen"] = 1 if update_data["fullscreen"] else 0

        for key, value in update_data.items():
            setattr(db_instance, key, value)
        db_instance.updated_at = datetime.utcnow()

        await self.db.commit()
        await self.db.refresh(db_instance)
        return InstanceResponse.model_validate(db_instance)

    async def delete(self, instance_id: str) -> bool:
        result = await self.db.execute(select(InstanceModel).where(InstanceModel.id == instance_id))
        db_instance = result.scalar_one_or_none()
        if not db_instance:
            return False
        await self.db.delete(db_instance)
        await self.db.commit()
        return True

    async def launch(self, instance_id: str) -> Optional[InstanceResponse]:
        result = await self.db.execute(select(InstanceModel).where(InstanceModel.id == instance_id))
        db_instance = result.scalar_one_or_none()
        if not db_instance:
            return None

        db_instance.status = InstanceStatus.LAUNCHING
        db_instance.last_played = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(db_instance)
        return InstanceResponse.model_validate(db_instance)

    async def get_launch_info(self, instance_id: str) -> Optional[dict]:
        """Get launch information including detected Java and launch command."""
        result = await self.db.execute(select(InstanceModel).where(InstanceModel.id == instance_id))
        db_instance = result.scalar_one_or_none()
        if not db_instance:
            return None

        # Detect suitable Java for this instance's Minecraft version
        java_info = java_detection_service.find_suitable_java(db_instance.version)

        # Determine Java executable to use
        java_executable = db_instance.java_version
        java_detected = None
        if java_info:
            java_detected = {
                "path": java_info.path,
                "version": java_info.version,
                "major_version": java_info.major_version,
                "is_jdk": java_info.is_jdk,
            }
            java_executable = java_info.path
        elif db_instance.java_version:
            java_executable = db_instance.java_version

        # Build launch command (simplified - real implementation would be more complex)
        launch_command = self._build_launch_command(db_instance, java_executable)

        return {
            "instance": InstanceResponse.model_validate(db_instance),
            "java_detected": java_detected,
            "java_executable": java_executable,
            "launch_command": launch_command,
            "required_java_version": java_detection_service._get_required_java_version(db_instance.version),
        }

    def _build_launch_command(self, instance: InstanceModel, java_executable: str) -> List[str]:
        """Build the Java command to launch Minecraft."""
        cmd = [java_executable]

        # Memory settings
        cmd.extend([f"-Xms{instance.memory_min}M", f"-Xmx{instance.memory_max}M"])

        # JVM arguments for Minecraft
        cmd.extend([
            "-XX:+UseG1GC",
            "-XX:+UnlockExperimentalVMOptions",
            "-XX:G1NewSizePercent=20",
            "-XX:G1ReservePercent=20",
            "-XX:MaxGCPauseMillis=50",
            "-XX:G1HeapRegionSize=32M",
        ])

        # Game directory
        if instance.game_dir:
            cmd.extend(["-Duser.dir", instance.game_dir])

        # Main class placeholder - real implementation would resolve from version manifest
        cmd.extend(["-cp", "\"libraries/*\"", "net.minecraft.client.main.Main"])

        # Game arguments
        cmd.extend([
            "--username", "Player",
            "--version", instance.version,
            "--gameDir", instance.game_dir or ".",
            "--assetsDir", "assets",
            "--assetIndex", instance.version,
            "--uuid", "00000000-0000-0000-0000-000000000000",
            "--accessToken", "0",
            "--userType", "legacy",
            "--versionType", "Prism Hub",
        ])

        if instance.fullscreen:
            cmd.append("--fullscreen")

        cmd.extend(["--width", str(instance.resolution_width)])
        cmd.extend(["--height", str(instance.resolution_height)])

        return cmd