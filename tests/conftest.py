import pytest


@pytest.fixture
def sample_list_of_dict() -> list[dict]:
    """Фикстура с данными для фильтрации"""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "RUB", "code": "RUB"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "EUR", "code": "EUR"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 245561903,
            "state": "EXECUTED",
            "date": "2020-01-15T11:45:12.105432",
            "amount": "1500.00",
            "currency_name": "RUB",
            "currency_code": "RUB",
            "description": "Оплата услуг",
            # "from": "Счет 45612378901234567890",
            "to": "Счет 98765432109876543210",
        },
        {
            "id": 558910244,
            "state": "CANCELED",
            "date": "2021-08-22T16:05:30.994112",
            "operationAmount": {"currency": {"name": "RUB", "code": "RUB"}},
            "description": "Перевод другу",
            "from": "Счет 11223344556677889900",
            "to": "Счет 55667788990011223344",
        },
    ]
