from typing import Iterator


def looking_name_of_currency(dct: dict, target_key: str = "currency") -> str | None:
    """Функция, возвращающая наименование валюты, если она есть в словаре"""
    if not isinstance(dct, dict):
        return None
    if target_key in dct:
        currency_data = dct[target_key]
        if isinstance(currency_data, dict):
            return currency_data.get("name")
        elif isinstance(currency_data, str):
            return currency_data
    for value in dct.values():
        result = looking_name_of_currency(value, target_key)
        if result is not None:
            return result
    return None


def filter_by_currency(data: list[dict], currency_name: str) -> Iterator[dict]:
    """Возвращает итератор словарей, отобранных по наименованию валюты"""
    return (el for el in data if looking_name_of_currency(el) == currency_name)


def transaction_descriptions(transactions: list[dict]) -> Iterator[str]:
    """Принимает список транзакций и поочередно возвращает их описания"""
    for transaction in transactions:
        yield transaction.get("description", "")


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """Генерирует номера карт в заданном диапазоне"""
    if end < start:
        start, end = end, start
    for i in range(start, end + 1):
        number = str(i).zfill(16)
        yield f"{number[:4]} {number[4:8]} {number[8:12]} {number[12:]}"
