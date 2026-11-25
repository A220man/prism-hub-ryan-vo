import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.database import init_db, engine, async_session_maker
from app.models.mod_profile_db import ModProfileModel
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
        await session.execute(delete(ModProfileModel))
        await session.commit()
    yield


@pytest.mark.asyncio
async def test_create_mod_profile(client, clean_db):
    """Test creating a new mod profile."""
    json = {
        "name": "Forge 1.20.1",
        "description": "Forge mod loader for Minecraft 1.20.1",
        "game_version": "1.20.1",
        "loader": "forge",
        "loader_version": "43.2.0",
    }
    response = await client.post("/api/v1/mod-profiles/", json=json)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Forge 1.20.1"
    assert data["game_version"] == "1.20.1"
    assert data["loader"] == "forge"
    assert "id" in data


@pytest.mark.asyncio
async def test_list_mod_profiles(client, clean_db):
    """Test listing mod profiles."""
    # Create a mod profile
    await client.post("/api/v1/mod-profiles/", json={
        "name": "Forge 1.20.1",
        "game_version": "1.20.1",
        "loader": "forge",
    })
    # Create another
    await client.post("/api/v1/mod-profiles/", json={
        "name": "Fabric 1.20.1",
        "game_version": "1.20.1",
        "loader": "fabric",
    })
    
    response = await client.get("/api/v1/mod-profiles/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


@pytest.mark.asyncio
async def test_get_mod_profile(client, clean_db):
    """Test getting a specific mod profile."""
    create_resp = await client.post("/api/v1/mod-profiles/", json={
        "name": "Test Profile",
        "game_version": "1.20.1",
        "loader": "forge",
    })
    mod_id = create_resp.json()["id"]
    
    response = await client.get(f"/api/v1/mod-profiles/{mod_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Profile"


@pytest.mark.asyncio
async def test_get_nonexistent_mod_profile(client, clean_db):
    """Test getting a mod profile that doesn't exist."""
    response = await client.get("/api/v1/mod-profiles/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_mod_profile(client, clean_db):
    """Test updating a mod profile."""
    create_resp = await client.post("/api/v1/mod-profiles/", json={
        "name": "Original",
        "game_version": "1.20.1",
        "loader": "forge",
    })
    mod_id = create_resp.json()["id"]
    
    update_data = {
        "name": "Updated Profile",
        "game_version": "1.20.2",
        "loader": "forge",
        "description": "Updated description",
    }
    response = await client.patch(f"/api/v1/mod-profiles/{mod_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Profile"
    assert data["game_version"] == "1.20.2"
    assert data["description"] == "Updated description"


@pytest.mark.asyncio
async def test_delete_mod_profile(client, clean_db):
    """Test deleting a mod profile."""
    create_resp = await client.post("/api/v1/mod-profiles/", json={
        "name": "To Delete",
        "game_version": "1.20.1",
        "loader": "forge",
    })
    mod_id = create_resp.json()["id"]
    
    delete_resp = await client.delete(f"/api/v1/mod-profiles/{mod_id}")
    assert delete_resp.status_code == 204
    
    # Verify it's gone
    get_resp = await client.get(f"/api/v1/mod-profiles/{mod_id}")
    assert get_resp.status_code == 404
