from unittest.mock import patch

import pytest

from src.generators import filter_by_currency, get_currency_code, looking_target_key
from src.main import (
    choose_status,
    clarify_selection,
    first_filtration,
    get_correct_answer,
    main,
    second_filtration,
    start,
)
from src.processing import process_bank_search, sort_by_date
from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "variants, expected",
    [
        ("1", "JSON-файл"),
        ("2", "CSV-файл"),
        ("3", "XLSX-файл"),
    ],
)
def test_start(variants: str, expected: str) -> None:
    with patch("builtins.input", return_value=variants) as mock_input:
        assert start() == expected
        mock_input.assert_called_once()


def test_start_with_wrong_input() -> None:
    with patch("builtins.input", side_effect=["4", "5", "a", "2"]) as mock_input:
        assert start() == "CSV-файл"
        assert mock_input.call_count == 4


@pytest.mark.parametrize(
    "variants, expected",
    [
        ("EXECUTED", "EXECUTED"),
        ("canceled", "CANCELED"),
        ("Pending", "PENDING"),
    ],
)
def test_choose_status(variants: str, expected: str) -> None:
    with patch("builtins.input", return_value=variants) as mock_input:
        assert choose_status() == expected
        mock_input.assert_called_once()


def test_choose_status_with_wrong_input() -> None:
    with patch("builtins.input", side_effect=["FIRST", "second", "CANCELED"]) as mock_input:
        assert choose_status() == "CANCELED"
        assert mock_input.call_count == 3


@pytest.mark.parametrize(
    "variants, correct_answers, expected",
    [
        ("да", {"нет": False, "да": True}, True),
        ("ДА", {"нет": False, "да": True}, True),
        ("Нет", {"нет": False, "да": True}, False),
        ("по возрастанию", {"по возрастанию": False, "по убыванию": True}, False),
        ("ПО возрастанию", {"по возрастанию": False, "по убыванию": True}, False),
        ("по УБЫВАНИЮ", {"по возрастанию": False, "по убыванию": True}, True),
    ],
)
def test_get_correct_answer(variants: str, correct_answers: dict, expected: bool) -> None:
    with patch("builtins.input", return_value=variants) as mock_input:
        assert get_correct_answer(correct_answers, "") == expected
        mock_input.assert_called_once()


def test_get_correct_answer_with_wrong_input() -> None:
    with patch("builtins.input", side_effect=["NO", "не знаю", "да"]) as mock_input:
        assert get_correct_answer({"нет": False, "да": True}, "") is True
        assert mock_input.call_count == 3


@pytest.mark.parametrize(
    "gets, expected, mock_chek",
    [
        (["да", "по Убыванию", "Да", "да", "word"], (True, True, True, "word"), 5),
        (["да", "ПО возрастанию", "Да", "Да", "WoRd"], (True, False, True, "word"), 5),
        (["нет", "нет", "Нет"], (False, True, False, None), 3),
    ],
)
def test_clarify_selection(gets: list, expected: tuple, mock_chek: int) -> None:
    with patch("builtins.input", side_effect=gets) as mock_input:
        assert clarify_selection() == expected
        assert mock_input.call_count == mock_chek


@pytest.mark.parametrize(
    "status, expected_indices",
    [
        ("EXECUTED", [0, 1, 2]),
        ("CANCELED", [3]),
        ("PENDING", []),
    ],
)
def test_first_filtration(sample_list_of_dict: list[dict], status: str, expected_indices: list) -> None:
    expected_data = [sample_list_of_dict[i] for i in expected_indices]
    with patch("src.main.start", return_value="JSON-файл"):
        with patch("src.main.read_file", return_value=sample_list_of_dict):
            with patch("src.main.choose_status", return_value=status):
                assert first_filtration() == (expected_data, True)


def test_first_filtration_empty_list() -> None:
    with patch("src.main.start", return_value="JSON-файл"):
        with patch("src.main.read_file", return_value=[]):
            assert first_filtration() == ([], False)


@pytest.mark.parametrize(
    "returned_selections, expected_indices",
    [
        ((True, True, True, "перевод"), [3, 0]),
        ((True, False, False, None), [0, 1, 2, 3]),
        ((False, True, False, None), [0, 1, 2, 3]),
    ],
)
def test_second_filtration(
    sample_list_of_dict: list[dict], returned_selections: tuple, expected_indices: list
) -> None:
    expected_data = [sample_list_of_dict[i] for i in expected_indices]
    with patch("src.main.clarify_selection", return_value=returned_selections):
        with patch("src.main.sort_by_date", wraps=sort_by_date) as mock_sort:
            with patch("src.main.filter_by_currency", wraps=filter_by_currency) as mock_currency:
                with patch("src.main.process_bank_search", wraps=process_bank_search) as mock_search:
                    assert second_filtration(sample_list_of_dict) == expected_data
    assert mock_sort.called == returned_selections[0]
    assert mock_currency.called == returned_selections[2]
    assert mock_search.called == bool(returned_selections[3])


@pytest.mark.parametrize(
    "returned_first, message",
    [
        (([], True), "Не найдено ни одной транзакции, подходящей под ваши условия фильтрации"),
        (([], False), "Файл не найден, не может быть прочитан или пустой"),
    ],
)
def test_main_sample_only_first_filter(
    returned_first: tuple, message: str, capsys: pytest.CaptureFixture[str]
) -> None:
    with patch("src.main.first_filtration", return_value=returned_first):
        with patch("src.main.second_filtration") as mock_second:
            main()
            captured = capsys.readouterr()
            assert captured.out.strip() == message
            mock_second.assert_not_called()


def test_main_first_filter_no_second(capsys: pytest.CaptureFixture[str]) -> None:
    with patch("src.main.first_filtration", return_value=(["тестовый_словарь"], True)):
        with patch("src.main.second_filtration", return_value=[]):
            main()
            captured = capsys.readouterr()
            assert captured.out.strip() == "Не найдено ни одной транзакции, подходящей под ваши условия фильтрации"


@pytest.mark.parametrize("indices", [0, 2])
def test_main(sample_list_of_dict: list, indices: int, capsys: pytest.CaptureFixture[str]) -> None:
    test_data = sample_list_of_dict[indices]
    with patch("src.main.first_filtration", return_value=([test_data], True)):
        with patch("src.main.second_filtration", return_value=[test_data]):
            main()
    captured = capsys.readouterr()
    assert "Распечатываю итоговый список транзакций..." in captured.out
    assert "Всего банковских операций в выборке: 1" in captured.out

    # Проверяем дату и описание
    assert f"{get_date(test_data['date'])} {test_data['description']}" in captured.out

    # Проверяем счета
    to_account = mask_account_card(looking_target_key(test_data, "to"))

    if "from" in test_data:
        from_account = mask_account_card(looking_target_key(test_data, "from"))
        assert f"{from_account} -> {to_account}" in captured.out
    else:
        assert to_account in captured.out
        assert " -> " not in captured.out

    # Проверяем сумму и валюту
    amount = looking_target_key(test_data, "amount")
    currency = get_currency_code(test_data)

    assert f"Сумма: {amount} {currency}" in captured.out
