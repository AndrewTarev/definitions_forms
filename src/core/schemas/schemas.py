import re
from typing import Dict

from fastapi import HTTPException
from pydantic import BaseModel, field_validator

from src.core.utils.logging_config import my_logger

# Регулярные выражения для определения типа данных
EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"
PHONE_REGEX_W_SPACE = r"^\+7 \d{3} \d{3} \d{2} \d{2}$"
PHONE_REGEX_WITHOUT_SPACE = r"^\+7\d{10}$"
DATE_REGEX = r"^(?:\d{4}-\d{2}-\d{2})|(?:\d{2}\.\d{2}\.\d{4})$"


def infer_field_type(value: str) -> str:
    """Определить тип поля (email, phone, date или text)."""
    try:
        if re.match(DATE_REGEX, value):
            return "date"
        elif re.match(PHONE_REGEX_W_SPACE, value) or re.match(
            PHONE_REGEX_WITHOUT_SPACE, value
        ):
            return "phone"
        elif re.match(EMAIL_REGEX, value):
            return "email"
        else:
            return "text"
    except Exception as e:
        my_logger.error(e)
        raise HTTPException(status_code=422, detail="Invalid type request data")


class FormData(BaseModel):
    """Модель шаблона формы."""

    data_form: Dict[str, str]

    @field_validator("data_form", mode="before")
    @classmethod
    def validate_phone_num(cls, v: Dict[str, str]) -> Dict[str, str]:
        form_type = dict()
        for key, value in v.items():
            type_val = infer_field_type(value)
            form_type[key] = type_val
        return form_type


class ResponseData(BaseModel):
    response: Dict[str, str]
