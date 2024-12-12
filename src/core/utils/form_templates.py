import asyncio
import json
import os.path

from pymongo import errors

from src.core.config import settings
from src.core.db_helper import db_helper
from src.core.utils.logging_config import my_logger


async def insert_documents() -> None:
    """Записывет шаблоны в БД"""
    try:
        await db_helper.connect_mongo()
        db = await db_helper.get_db()
        collection = db[settings.mongoDB.mongo_collection]
        await collection.create_index("name", unique=True)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        path_to_template = os.path.join(current_dir, "form.json")

        with open(path_to_template, "r") as f:
            sample_resource_json = json.load(f)
            result = await collection.insert_many(sample_resource_json)

        if result.inserted_ids:
            my_logger.info(
                f"Documents successfully inserted. Inserted IDs: {result.inserted_ids}"
            )
    except errors.BulkWriteError:
        # Обработка ошибок вставки из-за нарушения уникальности
        my_logger.info("Template forms already exists")

    except Exception as e:
        my_logger.error(f"An error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(insert_documents())
