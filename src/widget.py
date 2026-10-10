from datetime import datetime

from masks import get_mask_account, get_mask_card_number


def mask_account_card(info: str) -> str:
    """Функция обрабатывающая информацию о картах и счетах"""

    try:
        category, number = info.split()
    except ValueError:
        return 'Данные введены неверно'
    if category.lower() == "счет":
        return " ".join([category, get_mask_account(number)])
    return " ".join([category, get_mask_card_number(number)])


def get_date(info_date: str) -> str:
    date_object = datetime.fromisoformat(info_date)
    return date_object.strftime("%d.%m.%Y")
