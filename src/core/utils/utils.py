from typing import Dict, List

from fastapi import HTTPException

from src.core.utils.logging_config import my_logger


def matching_template(
    templates_list: List[dict], data: Dict[str, str]
) -> dict[str, str] | None:
    """Ищет совпадения присланных данных с нашими шаблонами"""
    try:
        i = 0
        matching_templates = {}  # Список для хранения всех подходящих шаблонов
        for template in templates_list:
            is_valid = True
            for key, value in template.get("fields", {}).items():
                # Проверяем, совпадает ли ключ и значение в переданных данных формы
                if key not in data or data[key] != value:
                    is_valid = False
                    break
            if is_valid:
                i += 1
                # Если шаблон валиден, добавляем его имя в словарь совпадений
                matching_templates[f"template_name{i}"] = template["name"]

        if len(matching_templates) != 0:
            return matching_templates
        return None

    except Exception as e:
        my_logger.error(e)
        raise HTTPException(status_code=400, detail="Error matching template")


def data_without_a_template(data: Dict[str, str]) -> Dict[str, str]:
    """Обрабатывает данные не нашедшие нужного шаблона"""
    try:
        i = 0
        new_data = dict()
        for value in data.values():
            i += 1
            new_data[f"f_name{i}"] = value
        return new_data
    except Exception as e:
        my_logger.error(e)
        raise HTTPException(status_code=400, detail="Data processing failed")
