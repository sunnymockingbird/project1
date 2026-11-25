from collections import Counter

import pytest

from src.processing import filter_by_state, process_bank_operations, process_bank_search, sort_by_date


@pytest.fixture
def sample_data() -> list[dict]:
    """Фикстура с тестовыми данными для фильтрации"""
    return [
        {"id": 1234, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 4875, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 3147599, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 144875, "state": "PENDING", "date": "2020-11-15T10:14:00.123456"},
        {"id": 99999, "state": "PENDING"},
    ]


@pytest.mark.parametrize(
    "state, expected_count, expected_ids",
    [
        ("EXECUTED", 2, [1234, 3147599]),
        ("CANCELED", 1, [4875]),
        ("PENDING", 2, [144875, 99999]),
        ("NONE", 0, []),
    ],
)
def test_filter_by_state(
    sample_data: list[dict], state: str, expected_count: int, expected_ids: list[int | None]
) -> None:
    result = filter_by_state(sample_data, state)
    assert len(result) == expected_count
    assert [item["id"] for item in result] == expected_ids


def test_filter_by_state_1() -> None:
    assert filter_by_state([], "EXECUTED") == []


def test_filter_by_state_2(sample_data: list[dict]) -> None:
    result = filter_by_state(sample_data)
    assert len(result) == 2
    assert [item["id"] for item in result] == [1234, 3147599]


def test_sort_by_date(sample_data: list[dict]) -> None:
    result = sort_by_date(sample_data)
    assert [item["id"] for item in result] == [144875, 1234, 4875, 3147599, 99999]


sorting_test_data = [
    {"id": 1234, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 4875, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 3147599, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 144875, "state": "PENDING", "date": "2020-11-15T10:14:00.123456"},
]


@pytest.mark.parametrize(
    "data, descending, expected_ids",
    [
        (sorting_test_data, False, [3147599, 4875, 1234, 144875]),  # По возрастанию (от 2018 к 2020)
        (sorting_test_data, True, [144875, 1234, 4875, 3147599]),  # По убыванию (от 2020 к 2018)
        ([], True, []),  # Пустой список
    ],
)
def test_sort_by_date_1(data: list[dict], descending: bool, expected_ids: list[int]) -> None:
    result = sort_by_date(data, descending)
    assert [item["id"] for item in result] == expected_ids


def test_process_bank_search_one_match(sample_list_of_dict: list[dict]) -> None:
    result = process_bank_search(sample_list_of_dict, "оплата")
    assert result == [sample_list_of_dict[2]]


def test_process_bank_search_few_matches(sample_list_of_dict: list[dict]) -> None:
    result = process_bank_search(sample_list_of_dict, "перевод")
    assert result == sample_list_of_dict[0:2] + [sample_list_of_dict[3]]


def test_process_bank_search_no_matches(sample_list_of_dict: list[dict]) -> None:
    result = process_bank_search(sample_list_of_dict, "пополнение")
    assert result == []


@pytest.fixture
def sample_operations() -> list[dict]:
    """Фикстура для проверки process_bank_operations"""
    return [
        {"description": "Перевод организации"},
        {"description": "Перевод организации"},
        {"description": "Перевод со счета на счет"},
        {"description": "Оплата услуг"},
        {"description": "Перевод другу"},
        {"description": "Оплата услуг"},
    ]


@pytest.mark.parametrize(
    "categories, expected",
    [
        (["Перевод организации", "Оплата услуг"], Counter({"Перевод организации": 2, "Оплата услуг": 2})),
        (["Перевод организации", "Пополнение счета"], Counter({"Перевод организации": 2, "Пополнение счета": 0})),
        (["Пополнение счета", "Оплата за товар"], Counter({"Пополнение счета": 0, "Оплата за товар": 0})),
        ([], Counter([])),
    ],
)
def test_process_bank_operations(sample_operations: list[dict], categories: list, expected: Counter) -> None:
    result = process_bank_operations(sample_operations, categories)
    assert result == expected
