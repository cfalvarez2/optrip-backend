import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_root(client: AsyncClient) -> None:
    response = await client.get("/v1")
    assert response.status_code == 200
    assert response.json() == {'key': "Hello world from API"}
