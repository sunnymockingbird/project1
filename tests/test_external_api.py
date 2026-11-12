from unittest.mock import patch

import pytest

from src.external_api import convert


@pytest.mark.parametrize(
    "transaction, expected",
    [
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
            884166.3,
        ),
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
            7911493.0,
        ),
    ],
)
def test_convert(transaction: dict, expected: float) -> None:
    """Тест конвертации рублевой транзакции"""
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"result": expected}
        assert convert(transaction) == expected


def test_convert_rub() -> None:
    """Тест конвертации рублевой транзакции (без обращения к API)"""
    transaction = {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {"amount": "9824.07", "currency": {"name": "RUB", "code": "RUB"}},
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702",
    }

    with patch("requests.get") as mock_get:
        assert convert(transaction) == 9824.07
        mock_get.assert_not_called()
