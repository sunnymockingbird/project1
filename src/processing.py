import re
from collections import Counter
from operator import itemgetter


def filter_by_state(data: list[dict], state: str = "EXECUTED") -> list[dict]:
    """Функция, фильтрующая список словарей по значению ключа state"""
    return [item for item in data if item.get("state") == state]


def sort_by_date(data: list[dict], descending: bool = True) -> list[dict]:
    """Функция, сортирующая словари по значению ключа date"""
    with_date = [item for item in data if "date" in item]
    without_date = [item for item in data if "date" not in item]
    return sorted(with_date, key=itemgetter("date"), reverse=descending) + without_date


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """Ищет подстроку в описании транзакций без учёта регистра. Возвращает список словарей, содержащих совпадение."""
    pattern = re.compile(re.escape(search), re.IGNORECASE)
    filtered_data = [el for el in data if pattern.search(el.get("description", ""))]
    return filtered_data


def process_bank_operations(data: list[dict], categories: list) -> dict:
    """Подсчитывает количество операций по заданным категориям.
    Возвращает Counter с количеством операций для каждой категории."""
    operations = [el["description"] for el in data if el["description"] in categories]
    result = Counter(operations)
    result.update(dict.fromkeys(categories, 0))
    return result
