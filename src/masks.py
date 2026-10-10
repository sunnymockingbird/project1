def get_mask_card_number(card_number: str) -> str:
    """Функция, маскирующая номер банковской карты в вид ХХХХ ХХ** **** ХХХХ"""

    if len(card_number) != 16:
        return "Номер карты введен некорректно"
    masked_number = card_number[:4] + " " + card_number[4:6] + "** ****" + card_number[-4:]
    return masked_number


def get_mask_account(account: str) -> str:
    """Функция, маскирующая номер банковского счета в вид **ХХХХ"""

    if len(account) < 4:
        return "Номер счета введен некорректно"
    masked_account = "**" + str(account)[-4:]
    return masked_account
