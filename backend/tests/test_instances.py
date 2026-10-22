import pytest
from sqlalchemy import select
from app.models.instance import InstanceStatus
@pytest.mark.asyncio
async def test_create_instance(client, clean_db):
    response = await client.post(
        "/api/v1/instances",
        json={
            "name": "Test Instance",
            "version": "1.20.1",
            "loader": "fabric",
            "loader_version": "0.15.11",
            "memory_min": 1024,
            "memory_max": 4096,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Instance"
    assert data["version"] == "1.20.1"
    assert data["loader"] == "fabric"
    assert data["status"] == "created"
    assert "id" in data


@pytest.mark.asyncio
async def test_list_instances(client, clean_db):
    # Create a few instances
    for i in range(3):
        await client.post("/api/v1/instances", json={"name": f"Instance {i}", "version": "1.20.1"})

    response = await client.get("/api/v1/instances")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3
    assert len(data["instances"]) == 3


@pytest.mark.asyncio
async def test_get_instance(client, clean_db):
    create_resp = await client.post("/api/v1/instances", json={"name": "Get Test", "version": "1.20.1"})
    instance_id = create_resp.json()["id"]

    response = await client.get(f"/api/v1/instances/{instance_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == instance_id
    assert data["name"] == "Get Test"


@pytest.mark.asyncio
async def test_get_nonexistent_instance(client, clean_db):
    response = await client.get("/api/v1/instances/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_instance(client, clean_db):
    create_resp = await client.post("/api/v1/instances", json={"name": "Original", "version": "1.20.1"})
    instance_id = create_resp.json()["id"]

    response = await client.patch(f"/api/v1/instances/{instance_id}", json={"name": "Updated", "memory_max": 8192})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated"
    assert data["memory_max"] == 8192


@pytest.mark.asyncio
async def test_delete_instance(client, clean_db):
    create_resp = await client.post("/api/v1/instances", json={"name": "To Delete", "version": "1.20.1"})
    instance_id = create_resp.json()["id"]

    response = await client.delete(f"/api/v1/instances/{instance_id}")
    assert response.status_code == 204

    get_resp = await client.get(f"/api/v1/instances/{instance_id}")
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_launch_instance(client, clean_db):
    create_resp = await client.post("/api/v1/instances", json={"name": "Launch Test", "version": "1.20.1"})
    instance_id = create_resp.json()["id"]

    response = await client.post(f"/api/v1/instances/{instance_id}/launch")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "launching"
    assert data["last_played"] is not None