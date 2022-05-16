import pytest
import pytest_asyncio
import asyncio
from typing import AsyncIterator
from httpx import AsyncClient
from os import environ
from fastapi import FastAPI

environ["PY_ENV"] = "testing"
environ["DB_NAME"] = f"{environ['DB_NAME']}_test"

from src import app  # noqa: E402


async def clear_database(server: FastAPI) -> None:
    """Empties the test database"""
    for collection in await server.db.list_collections():
        await server.db[collection["name"]].delete_many({})


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def client() -> AsyncIterator[AsyncClient]:
    """Async server client that handles lifespan and teardown"""
    async with AsyncClient(app=app, base_url="http://test") as _client:
        try:
            yield _client
        except Exception as exc:  # pylint: disable=broad-except
            print(exc)
        finally:
            await clear_database(app)
