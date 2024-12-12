import json
import logging
import os
from pathlib import Path

from mongomock_motor import AsyncMongoMockClient

from src.core.config import settings


class MongoHandler:
    settings.mongoDB.testing = True

    def __init__(
        self, db_name: str, collection_name: str, db_client: AsyncMongoMockClient
    ):
        self.__db_name = db_name
        self.__collection_name = collection_name
        self.__db_client = db_client

    async def insert_sample_resource(self, sample_resource: list):
        await self.__db_client[self.__db_name][self.__collection_name].insert_many(
            sample_resource
        )

    async def drop_database(self):
        await self.__db_client.drop_database(self.__db_name)

    def close_conn(self):
        self.__db_client.close()


class MongoClient:
    def __init__(
        self, db_name: str, collection_name: str, db_client: AsyncMongoMockClient
    ):
        self.__db_handler = MongoHandler(db_name, collection_name, db_client)

    async def __aenter__(self):
        await self.__create_mock_data()
        return self.__db_handler

    async def __create_mock_data(self):
        base_dir = Path(__file__).resolve().parent.parent
        path_to_template = os.path.join(base_dir, "src/core/utils/form.json")
        with open(path_to_template, "r") as f:
            sample_resource_json = json.load(f)
            await self.__db_handler.insert_sample_resource(sample_resource_json)

    async def __aexit__(self, exception_type, exception_value, exception_traceback):
        if exception_type:
            logging.error(exception_value)

        await self.__db_handler.drop_database()
        self.__db_handler.close_conn()
