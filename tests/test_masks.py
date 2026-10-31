import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    "number_card, expected",
    [
        ("7000792289606361", "7000 79** **** 6361"),
        ("1234567890123456", "1234 56** **** 3456"),
        ("5555444433332222", "5555 44** **** 2222"),
        ("2200123456789012", "2200 12** **** 9012"),
        ("", "Номер карты введен некорректно"),
        ("220012345678901", "Номер карты введен некорректно"),
        ("22001234567890581", "Номер карты введен некорректно"),
    ],
)
def test_get_mask_card_number(number_card, expected):
    assert get_mask_card_number(number_card) == expected


@pytest.mark.parametrize(
    "account_number, expected",
    [
        ("73654108430135874305", "**4305"),
        ("12345678901234567890", "**7890"),
        ("", "Номер счета введен некорректно"),
        ("758", "Номер счета введен некорректно"),
        ("7589", "**7589"),
        ("12345678911234567892123", "**2123"),
        ("8" * 99, "**8888"),
    ],
)
def test_get_mask_account(account_number, expected):
    assert get_mask_account(account_number) == expected
