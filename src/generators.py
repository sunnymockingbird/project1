from typing import Any, Iterator


def looking_target_key(dct: dict, target_key: str) -> Any:
    """Функция, возвращающая значение ключа, если он есть в словаре"""
    if not isinstance(dct, dict):
        return None
    if target_key in dct:
        value_of_key = dct[target_key]
        return value_of_key
    for value in dct.values():
        result = looking_target_key(value, target_key)
        if result is not None:
            return result
    return None


def get_currency_code(dct: dict) -> str | None:
    """Возвращает код валюты из словаря."""
    if "currency_code" in dct:
        result = dct["currency_code"]
        return result if isinstance(result, str) else None
    currency = looking_target_key(dct, "currency")
    if isinstance(currency, dict):
        result = currency.get("code")
        return result if isinstance(result, str) else None
    return None


def filter_by_currency(data: list[dict], currency_code: str) -> Iterator[dict]:
    """Возвращает итератор словарей, отобранных по коду валюты"""
    return (el for el in data if get_currency_code(el) == currency_code)


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
