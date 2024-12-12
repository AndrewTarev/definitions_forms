from typing import List, Dict

from fastapi import APIRouter, Depends, HTTPException, Request
from motor.motor_asyncio import AsyncIOMotorClient

from src.core.config import settings
from src.core.db_helper import db_helper
from src.core.schemas.schemas import FormData
from src.core.utils.logging_config import my_logger
from src.core.utils.utils import matching_template, data_without_a_template

router = APIRouter(
    tags=["Get_templates"],
)


@router.post(
    "/get_form",
)
async def get_form(
    form_data: Request,
    db: AsyncIOMotorClient = Depends(db_helper.get_db),
) -> dict[str, str]:
    """Определяет шаблон для переданных данных формы."""
    try:
        form_data = await form_data.form()
        valid_data = FormData(form_data=form_data)
    except Exception as e:
        my_logger.error(e)
        raise HTTPException(status_code=400, detail="Invalid form data")

    try:
        # Получаем наши шаблоны из MongoDB
        templates_cursor = await db.find().to_list(length=None)
        # Конвертируем ObjectId в строку
        templates: List[dict[str, str]] = [
            {**doc, "_id": str(doc["_id"])} for doc in templates_cursor
        ]
    except Exception as e:
        my_logger.error(e)
        raise HTTPException(status_code=400, detail="Invalid connection to mongodb")

    if template_name := matching_template(templates, valid_data.form_data):
        return template_name
    return data_without_a_template(valid_data.form_data)
