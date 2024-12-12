from typing import List

from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

from src.core.db_helper import db_helper
from src.core.schemas.schemas import FormData, ResponseData
from src.core.utils.logging_config import my_logger
from src.core.utils.utils import data_without_a_template, matching_template

router = APIRouter(
    tags=["Get_templates"],
)


@router.post("/get_form", response_model=ResponseData)
async def get_form(
    data: FormData,
    db: AsyncIOMotorClient = Depends(db_helper.get_db),
) -> dict[str, dict[str, str] | None] | dict[str, dict[str, str]]:
    """Определяет шаблон для переданных данных формы."""
    try:
        # Получаем наши шаблоны из MongoDB
        templates_cursor = await db.find().to_list(length=None)  # type: ignore
        # Конвертируем ObjectId в строку
        templates: List[dict[str, str]] = [
            {**doc, "_id": str(doc["_id"])} for doc in templates_cursor
        ]
    except Exception as e:
        my_logger.error(e)
        raise HTTPException(status_code=400, detail="Invalid connection to mongodb")

    if template_name := matching_template(templates, data.data_form):
        return {"response": template_name}
    data_type = data_without_a_template(data.data_form)
    return {"response": data_type}
