from unittest.mock import mock_open, patch

import pandas as pd
import pytest

from src.utils import read_file


@pytest.mark.parametrize(
    "file_name, mock_data, expected_data",
    [
        ("any_path.json", '[{"id": 1, "amount": "100"}]', [{"id": 1, "amount": "100"}]),
        ("any_path.csv", "id;amount\n1;100\n", [{"id": "1", "amount": "100"}]),
        ("any_path.xlsx", pd.DataFrame({"id": [1], "amount": ["100"]}), [{"id": 1, "amount": "100"}]),
    ],
)
def test_read_file_success(file_name: str, mock_data: str | pd.DataFrame, expected_data: list) -> None:
    """Тест успешного чтения валидного списка транзакций."""
    if not file_name.endswith("xlsx"):
        with patch("builtins.open", mock_open(read_data=mock_data)):
            assert read_file(file_name) == expected_data
    else:
        with patch("pandas.read_excel", return_value=mock_data):
            assert read_file(file_name) == expected_data


@pytest.mark.parametrize(
    "file_name, invalid_content",
    [
        ("any_path.json", ""),  # Пустой файл
        ("any_path.csv", ""),  # Пустой файл
        ("any_path.json", "[]"),  # Пустой список
        ("any_path.csv", "id;amount"),  # csv только с заголовками
        ("any_path.json", "{'id': 1}"),  # Словарь вместо списка
        ("any_path.json", '{"id": 1}'),  # Словарь вместо списка, но в формате json
        ("any_path.json", "не json текст"),  # Битый JSON
        ("any_path.csv", "не csv файл"),
        ("any_path.xlsx", pd.DataFrame()),  # Пустой excel-файл
        ("any_path.png", ""),  # Другой формат файла
    ],
)
def test_read_file_empty_list(file_name: str, invalid_content: str | pd.DataFrame) -> None:
    """Тест возврата пустого списка"""
    if not file_name.endswith("xlsx"):
        with patch("builtins.open", mock_open(read_data=invalid_content)):
            assert read_file(file_name) == []
    else:
        with patch("pandas.read_excel", return_value=invalid_content):
            assert read_file(file_name) == []


def test_read_file_not_found() -> None:
    """Тест случая ненайденного файла"""

    with patch("builtins.open", side_effect=FileNotFoundError):
        assert read_file("non_existent.json") == []
