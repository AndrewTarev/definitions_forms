from typing import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from mongomock_motor import AsyncMongoMockClient
from tests.mongo_client import MongoClient

from src.core.config import settings
from src.main import app

test_db_client = AsyncMongoMockClient()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def mongo_client() -> AsyncGenerator[MongoClient, None]:
    async with MongoClient(
        db_name=settings.mongoDB.test_name,
        collection_name=settings.mongoDB.test_collection,
        db_client=test_db_client,
    ) as mongo_client:
        yield mongo_client


@pytest_asyncio.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as async_client:
        yield async_client
