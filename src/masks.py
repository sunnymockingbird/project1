import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(BASE_DIR / "logs" / "utils.log", "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def get_mask_card_number(card_number: str) -> str:
    """Функция, маскирующая номер банковской карты в вид ХХХХ ХХ** **** ХХХХ"""
    if len(card_number) != 16 or not card_number.isdigit():
        logger.error("Номер карты был введен не верно")
        return "Номер карты введен некорректно"
    masked_number = card_number[:4] + " " + card_number[4:6] + "** ****" + " " + card_number[-4:]
    logger.info("Номер карты замаскирован и возвращен")
    return masked_number


def get_mask_account(account: str) -> str:
    """Функция, маскирующая номер банковского счета в вид **ХХХХ"""
    if len(account) < 4 or not account.isdigit():
        logger.error("Номер счета был введен не верно")
        return "Номер счета введен некорректно"
    masked_account = "**" + str(account)[-4:]
    logger.info("Номер счета замаскирован и возвращен")
    return masked_account
