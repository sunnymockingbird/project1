import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "user_input, expected",
    [
        ("Visa Gold 7000792289606361", "Visa Gold 7000 79** **** 6361"),
        ("Mastercard 1234567890123456", "Mastercard 1234 56** **** 3456"),
        ("Maestro 5555444433332222", "Maestro 5555 44** **** 2222"),
        ("МИР 2200123456789012", "МИР 2200 12** **** 9012"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("", "Данные введены неверно"),
        ("Visa Gold", "Данные введены неверно"),
        ("12345", "Данные введены неверно"),
    ],
)
def test_mask_account_card(user_input, expected):
    assert mask_account_card(user_input) == expected


@pytest.mark.parametrize(
    "date_string, expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2026-10-28T23:59:59.999999", "28.10.2026"),
        ("2025-01-05T12:00:00.000000", "05.01.2025"),
    ],
)
def test_get_date_success(date_string, expected):
    assert get_date(date_string) == expected


@pytest.mark.parametrize("bad_date", ["", "18/03/2025"])
def test_get_date_errors(bad_date):
    with pytest.raises(ValueError):
        get_date(bad_date)
