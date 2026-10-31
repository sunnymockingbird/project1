import pytest

from src.generators import (
    card_number_generator,
    filter_by_currency,
    looking_name_of_currency,
    transaction_descriptions,
)


@pytest.mark.parametrize(
    "data, expected",
    [
        # Тест 1: Валюта внутри словаря
        (
            {
                "id": 939719570,
                "state": "EXECUTED",
                "date": "2018-06-30T02:08:58.425572",
                "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
                "description": "Перевод организации",
                "from": "Счет 75106830613657916952",
                "to": "Счет 11776614605963066702",
            },
            "USD",
        ),
        # Тест 2: Другая валюта внутри словаря
        (
            {
                "id": 142264268,
                "state": "EXECUTED",
                "date": "2019-04-04T23:20:05.206878",
                "operationAmount": {"amount": "79114.93", "currency": {"name": "EUR", "code": "EUR"}},
                "description": "Перевод со счета на счет",
                "from": "Счет 19708645243227258542",
                "to": "Счет 75651667383060284188",
            },
            "EUR",
        ),
        # Тест 3: Валюта на верхнем уровне строкой
        ({"id": 142264268, "state": "EXECUTED", "currency": "RUB"}, "RUB"),
        # Тест 4: Валюты вообще нет в словаре
        (
            {
                "id": 142264268,
                "state": "EXECUTED",
                "date": "2019-04-04T23:20:05.206878",
                "operationAmount": {"amount": "79114.93"},
            },
            None,
        ),
    ],
)
def test_looking_name_of_currency(data, expected):
    assert looking_name_of_currency(data) == expected


@pytest.fixture
def sample_list_of_dict():
    """Фикстура с данными для фильтрации"""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
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
            "operationAmount": {"amount": "1500.00", "currency": {"name": "USD", "code": "USD"}},
            "description": "Оплата услуг",
            "from": "Счет 45612378901234567890",
            "to": "Счет 98765432109876543210",
        },
        {
            "id": 558910244,
            "state": "EXECUTED",
            "date": "2021-08-22T16:05:30.994112",
            "operationAmount": {"amount": "432.50", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод другу",
            "from": "Счет 11223344556677889900",
            "to": "Счет 55667788990011223344",
        },
    ]


def test_filter_by_currency(sample_list_of_dict):
    transactions_iterator = filter_by_currency(sample_list_of_dict, "USD")
    assert next(transactions_iterator)["id"] == 939719570
    assert next(transactions_iterator)["id"] == 245561903
    assert next(transactions_iterator)["id"] == 558910244


def test_filter_by_currency_with_empty_list():
    transactions_iterator = filter_by_currency([], "USD")
    with pytest.raises(StopIteration):
        next(transactions_iterator)


@pytest.fixture
def sample_of_transactions():
    """Фикстура для теста генератора транзакций"""
    return [
        {"description": "Перевод организации", "date": "2019-04-04T23:20:05.206878"},
        {"description": "Перевод со счета на счет", "date": "2019-04-04T23:20:05.206878"},
        {"description": "Перевод с карты на карту", "date": "2019-04-04T23:20:05.206878"},
    ]


def test_transaction_descriptions(sample_of_transactions):
    transactions = transaction_descriptions(sample_of_transactions)
    assert next(transactions) == "Перевод организации"
    assert next(transactions) == "Перевод со счета на счет"
    assert next(transactions) == "Перевод с карты на карту"


def test_transaction_descriptions_with_empty_list():
    transactions = transaction_descriptions([])
    with pytest.raises(StopIteration):
        next(transactions)


def test_card_number_generator():
    cards = card_number_generator(1, 3)
    assert next(cards) == "0000 0000 0000 0001"
    assert next(cards) == "0000 0000 0000 0002"
    assert next(cards) == "0000 0000 0000 0003"

    with pytest.raises(StopIteration):
        next(cards)


def test_card_number_generator_single_value():
    cards = card_number_generator(999, 999)
    assert next(cards) == "0000 0000 0000 0999"


def test_card_number_generator_large_number():
    cards = card_number_generator(9999, 10001)
    assert next(cards) == "0000 0000 0000 9999"
    assert next(cards) == "0000 0000 0001 0000"
    assert next(cards) == "0000 0000 0001 0001"


def test_card_number_generator_with_wrong_boundaries():
    cards = card_number_generator(3, 1)
    assert next(cards) == "0000 0000 0000 0001"
    assert next(cards) == "0000 0000 0000 0002"
    assert next(cards) == "0000 0000 0000 0003"
