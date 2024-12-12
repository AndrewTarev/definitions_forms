import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_type_validation(ac: AsyncClient) -> None:
    data = {
        "PhoneNumber1": "+7 123 456 78 90",
        "PhoneNumber2": "+71234567890",
        "Email": "some_mail@mail.ru",
        "Date1": "07.12.1996",
        "Date2": "1996-12-07",
        "Some_text": "some_text",
    }
    response = await ac.post("/get_form", data=data)
    data = response.json()

    assert response.status_code == 200
    assert data == {
        "f_name1": "phone",
        "f_name2": "phone",
        "f_name3": "email",
        "f_name4": "date",
        "f_name5": "date",
        "f_name6": "text",
    }


@pytest.mark.asyncio
async def test_type_invalid(ac: AsyncClient) -> None:
    data = {
        "PhoneNumber1": "+7 123 456",
        "PhoneNumber2": "81234567890",
        "Email": "some_mailmail.ru",
        "Date1": "07-12-1996",
        "Some_text": 89004030700,
    }

    response = await ac.post("/get_form", data=data)
    data = response.json()

    assert response.status_code == 200
    assert data == {
        "f_name1": "text",
        "f_name2": "text",
        "f_name3": "text",
        "f_name4": "text",
        "f_name5": "text",
    }


@pytest.mark.asyncio
async def test_find_first_template(ac: AsyncClient) -> None:
    order_form_1 = {
        "order_date": "1996-12-07",
        "phone": "+7 123 456 78 90",
        "lead_email": "some_mail@mail.ru",
        "text": "where_detonator?",
    }

    response = await ac.post("/get_form", data=order_form_1)
    data = response.json()

    assert response.status_code == 200
    assert data == {"template_name1": "Order_form_1"}


@pytest.mark.asyncio
async def test_find_second_template(ac: AsyncClient) -> None:
    order_form_2 = {
        "date_registry": "1996-12-07",
        "phone": "+7 123 456 78 90",
        "working_email": "some_mail@mail.ru",
    }

    response = await ac.post("/get_form", data=order_form_2)
    data = response.json()

    assert response.status_code == 200
    assert data == {"template_name1": "Order_form_2"}


@pytest.mark.asyncio
async def test_find_third_template(ac: AsyncClient) -> None:
    order_form_3 = {
        "date": "1996-12-07",
        "phone_number": "+7 123 456 78 90",
        "email": "some_mail@mail.ru",
    }

    response = await ac.post("/get_form", data=order_form_3)
    data = response.json()

    assert response.status_code == 200
    assert data == {"template_name1": "Order_form_3"}


@pytest.mark.asyncio
async def test_find_template_with_any_params(ac: AsyncClient) -> None:
    data = {
        "date": "1996-12-07",
        "phone_number": "+7 123 456 78 90",
        "email": "some_mail@mail.ru",
        "somthing_else": "some_text",
        1: "where_detonator?",
    }
    response = await ac.post("/get_form", data=data)
    data = response.json()

    assert response.status_code == 200
    assert data == {"template_name1": "Order_form_3"}


@pytest.mark.asyncio
async def test_find_all_template(ac: AsyncClient) -> None:
    order_form = {
        "order_date": "1996-12-07",
        "phone": "+7 123 456 78 90",
        "lead_email": "some_mail@mail.ru",
        "text": "where_detonator?",
        "date_registry": "1996-12-07",
        "working_email": "some_mail@mail.ru",
        "date": "1996-12-07",
        "phone_number": "+7 123 456 78 90",
        "email": "some_mail@mail.ru",
    }

    response = await ac.post("/get_form", data=order_form)
    data = response.json()

    assert response.status_code == 200
    assert data == {
        "template_name1": "Order_form_1",
        "template_name2": "Order_form_2",
        "template_name3": "Order_form_3",
    }
