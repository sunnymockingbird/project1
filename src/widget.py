from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(info: str) -> str:
    """Функция обрабатывающая информацию о картах и счетах"""
    parts = info.split()
    if len(parts) < 2 or not parts[-1].isdigit():
        return "Данные введены неверно"
    elif parts[0].lower() == "счет":
        return " ".join([*parts[:-1], get_mask_account(parts[-1])])
    return " ".join([*parts[:-1], get_mask_card_number(parts[-1])])


def get_date(info_date: str) -> str:
    date_object = datetime.fromisoformat(info_date)
    return date_object.strftime("%d.%m.%Y")
