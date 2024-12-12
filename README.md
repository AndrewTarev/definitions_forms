# Definitions forms

## Описание
Web-приложение для определения заполненных форм. 

В базе данных(MongoDB) хранится список шаблонов форм (шаблон можно посмотреть по пути: `src/core/utils/form.json`).

На вход по урлу /get_form POST запросом передаются данные в json формате:
```python
{
  "data_form": {
        "order_date": "1996-12-07",
        "phone": "+7 123 456 78 90",
        "lead_email": "some_mail@mail.ru",
        "text": "where_detonator?"
  }
}
```
В ответ возвращается имя наиболее подходящей данному списку полей формы:
```python
{
  "response": {
    "template_name1": "Order_form_1"
  }
}
```
При отсутствии совпадений с известными формами производится типизация 
полей на лету и вернуть список полей с их типами.
```python
{
  "response": {
    "f_name1": "date",
    "f_name2": "phone",
    "f_name3": "email",
    "f_name4": "text"
  }
}
```
Приложение протестировано и отформатированно линтерами (Black, isort, flake8, mypy)

## Технический стек:

- Python 3.12+
- FastAPI
- MongoDB
- Docker
- Poetry - для управления зависимостями
- Pytest
- mongomock-motor
- Loguru
- github ci

## Установка приложения:

1. Склонируйте репозиторий себе на компьютер
    - git clone https://github.com/AndrewTarev/definitions_forms

2. Запустите сборку контейнеров
    - docker-compose up --build

API документация (Swagger/OpenAPI) доступна по пути http://0.0.0.0:8000/docs
