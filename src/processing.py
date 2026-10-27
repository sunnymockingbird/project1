from operator import itemgetter


def filter_by_state(data: list[dict], state: str = "EXECUTED") -> list[dict]:
    """Функция, фильтрующая список словарей по значению ключа state"""

    return [item for item in data if item.get("state") == state]


def sort_by_date(data: list[dict], descending: bool = True) -> list[dict]:
    """Функция, сортирующая словари по значению ключа date"""
    with_date = [item for item in data if "date" in item]
    without_date = [item for item in data if "date" not in item]
    return sorted(with_date, key=itemgetter("date"), reverse=descending) + without_date
