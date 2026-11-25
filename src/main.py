import os

from src.generators import filter_by_currency, get_currency_code, looking_target_key
from src.processing import filter_by_state, process_bank_search, sort_by_date
from src.utils import read_file
from src.widget import get_date, mask_account_card

FILE_TYPES = {"1": "JSON-файл", "2": "CSV-файл", "3": "XLSX-файл"}
AVAILABLE_STATUSES = ["EXECUTED", "CANCELED", "PENDING"]
FILES = {"JSON-файл": "operations.json", "CSV-файл": "transactions.csv", "XLSX-файл": "transactions_excel.xlsx"}


def start() -> str:
    """Приветствует пользователя. Запрашивает у пользователя тип файла для обработки и возвращает его"""
    print("""Привет! Добро пожаловать в программу работы
с банковскими транзакциями.
Выберите необходимый пункт меню:
1. Получить информацию о транзакциях из JSON-файла
2. Получить информацию о транзакциях из CSV-файла
3. Получить информацию о транзакциях из XLSX-файла""")
    query = input("Введите 1, 2 или 3: ")
    while query not in FILE_TYPES:
        print("Вы ввели некорректное значение")
        query = input("Введите 1, 2 или 3: ")
    user_file_type = FILE_TYPES[query]
    return user_file_type


def choose_status() -> str:
    """Запрашивает у пользователя статус операции для фильтрации транзакций и возвращает его"""
    status = input("""Введите статус, по которому необходимо выполнить фильтрацию.
Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING""" "\n")
    while status.upper() not in AVAILABLE_STATUSES:
        print(f"Статус операции {status} недоступен.")
        status = input("""Введите статус, по которому необходимо выполнить фильтрацию.
        Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING""" "\n")
    status = status.upper()
    print(f'Операции отфильтрованы по статусу "{status}"')
    return status


def get_correct_answer(correct_answers: dict[str, bool], question: str) -> bool:
    """Запрашивает у пользователя ответ на вопрос и возвращает его булевое значение"""
    answer = input(f"{question}: ").strip().lower()
    while answer not in correct_answers:
        answer = input(f"{question}: ").strip().lower()
    return correct_answers[answer]


def clarify_selection() -> tuple[bool, bool, bool, str | None]:
    """Уточняет дополнительные параметры сортировки и фильтрации и возвращает их"""
    answers = {"нет": False, "да": True}
    sort_order = {"по возрастанию": False, "по убыванию": True}
    sorting_by_date = get_correct_answer(answers, "Отсортировать операции по дате? Да / Нет")
    if sorting_by_date:
        descending = get_correct_answer(sort_order, "Отсортировать по возрастанию или по убыванию?")
    else:
        descending = True
    rub_currency = get_correct_answer(answers, "Выводить только рублевые транзакции? Да / Нет")
    filter_key_bool = get_correct_answer(
        answers, "Отфильтровать список транзакций по определенному слову в описании? Да / Нет"
    )
    if filter_key_bool:
        filter_key = input("Введите слово для фильтрации: ").lower()
    else:
        filter_key = None
    return sorting_by_date, descending, rub_currency, filter_key


def first_filtration() -> tuple[list[dict], bool]:
    """Читает файл, производит первую фильтрацию по статусу операции.
    Возвращает отфильтрованный список словарей и флаг возможных проблем с открытием файла или отсутствия данных"""
    user_file_type = start()
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", FILES[user_file_type])
    data = read_file(file_path)
    flag_success = False
    if data:
        flag_success = True
        status = choose_status()
        filtered = filter_by_state(data, status)
        return filtered, flag_success
    return data, flag_success


def second_filtration(filtered: list[dict]) -> list[dict]:
    """Фильтрует список словарей по полученным параметрам и возвращает его"""
    sorting_by_date, descending, rub_currency, filter_key = clarify_selection()
    if sorting_by_date:
        filtered = sort_by_date(filtered, descending)
    if rub_currency:
        filtered = list(filter_by_currency(filtered, "RUB"))
    if filter_key:
        filtered = process_bank_search(filtered, filter_key)
    return filtered


def main() -> None:
    """Запускает обработку транзакций и выводит результаты фильтрации"""
    data, flag = first_filtration()
    if data:
        data = second_filtration(data)
        if not data:
            print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
            return
    else:
        if flag:
            print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        else:
            print("Файл не найден, не может быть прочитан или пустой")
        return
    print("Распечатываю итоговый список транзакций...")
    print(f"Всего банковских операций в выборке: {len(data)}")
    for el in data:
        print()
        date = get_date(el["date"])
        from_account = mask_account_card(looking_target_key(el, "from"))
        to_account = mask_account_card(looking_target_key(el, "to"))
        amount = looking_target_key(el, "amount")
        currency = get_currency_code(el)
        if not from_account.startswith("Данные введены"):
            print(f"{date} {el['description']}\n" f"{from_account} -> {to_account}\n" f"Сумма: {amount} {currency}\n")
        else:
            print(f"{date} {el['description']}\n" f"{to_account}\n" f"Сумма: {amount} {currency}\n")
