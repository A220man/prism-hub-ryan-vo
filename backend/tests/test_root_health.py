import pytest
@pytest.mark.asyncio
async def test_root_health(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "prism-hub-api"}