import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.database import init_db, engine, async_session_maker
from app.models.instance_db import InstanceModel
from sqlalchemy import delete


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db():
    await init_db()
    yield
    await engine.dispose()


@pytest_asyncio.fixture
async def clean_db():
    async with async_session_maker() as session:
        await session.execute(delete(InstanceModel))
        await session.commit()
    yield