import json
from unittest.mock import mock_open, patch

import pytest

from src.utils import read_file


def test_read_file_success() -> None:
    """Тест успешного чтения валидного списка транзакций."""
    expected_data = [{"id": 1, "amount": "100"}]
    mock_json_data = json.dumps(expected_data)

    with patch("builtins.open", mock_open(read_data=mock_json_data)):
        assert read_file("any_path.json") == expected_data


@pytest.mark.parametrize(
    "invalid_content",
    [
        "",  # Пустой файл
        "[]",  # Пустой список
        '{"id": 1}',  # Словарь вместо списка
        "не json текст",  # Битый JSON
    ],
)
def test_read_file_empty_list(invalid_content: str) -> None:
    """Тест возврата пустого списка"""

    with patch("builtins.open", mock_open(read_data=invalid_content)):
        assert read_file("any_path.json") == []


def test_read_file_not_found() -> None:
    """Тест случая ненайденного файла"""

    with patch("builtins.open", side_effect=FileNotFoundError):
        assert read_file("non_existent.json") == []
