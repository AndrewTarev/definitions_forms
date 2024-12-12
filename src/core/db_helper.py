import asyncio

from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase,
)

from src.core.config import settings
from src.core.utils.logging_config import my_logger


class DatabaseHelper:
    db_client: AsyncIOMotorClient

    def __init__(
        self,
        url: str,
        db_name: str,
        db_collection: str,
        maxPoolSize: int,
        minPoolSize: int,
    ) -> None:
        self.url = url
        self.db_name = db_name
        self.db_collection = db_collection
        self.maxPoolSize = maxPoolSize
        self.minPoolSize = minPoolSize

    async def get_db(self) -> AsyncIOMotorCollection | AsyncIOMotorDatabase:
        if settings.mongoDB.testing:
            # тестовая БД
            from tests.conftest import test_db_client

            mock_db: AsyncIOMotorDatabase = test_db_client[settings.mongoDB.test_name][
                settings.mongoDB.test_collection
            ]
            return mock_db
        # Основная БД
        return self.db_client[self.db_name][self.db_collection]

    async def connect_mongo(self) -> None:
        try:
            self.db_client = AsyncIOMotorClient(
                self.url,
                maxPoolSize=self.maxPoolSize,
                minPoolSize=self.minPoolSize,
            )
            my_logger.info("Connected to mongo.")
        except Exception as e:
            my_logger.error(f"Could not connect to mongo: {e}")
            raise

    async def close_mongo_connect(self) -> None:
        if self.db_client is None:
            my_logger.warning("Connection is None, nothing to close.")
            return
        self.db_client.close()
        my_logger.info("Mongo connection closed.")


# Настройка подключения к базе данных
db_helper = DatabaseHelper(
    url=str(settings.mongoDB.url),
    db_name=str(settings.mongoDB.mongo_db_name),
    db_collection=str(settings.mongoDB.mongo_collection),
    maxPoolSize=settings.mongoDB.mongo_max_connections,
    minPoolSize=settings.mongoDB.mongo_min_connections,
)

if __name__ == "__main__":
    asyncio.run(db_helper.connect_mongo())
