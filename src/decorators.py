from datetime import datetime
from functools import wraps
from typing import Any, Callable


def log(filename: str | None = None) -> Callable:
    '''Декоратор для логирования работы функций.
    Принимает необязательный аргумент filename (путь к файлу для логов).
    При успешном выполнении функции записывает в файл или выводит в консоль
    время вызова функции, в противном случае — имя и тип возникшей ошибки.
    """'''

    def wrapper(func: Callable) -> Callable:
        @wraps(func)
        def inner(*args: Any, **kwargs: Any) -> Any:
            try:
                start_time = datetime.now()
                result = func(*args, **kwargs)
                message = f"{start_time} {func.__name__} была вызвана и успешно завершила работу"
                if filename:
                    with open(filename, "a", encoding="utf-8") as file:
                        file.write(message + "\n")
                else:
                    print(message)
                return result
            except Exception as err:
                message = f"{func.__name__} error: {type(err).__name__}. Inputs: {args}, {kwargs}"
                if filename:
                    with open(filename, "a", encoding="utf-8") as file:
                        file.write(message + "\n")
                else:
                    print(message)
                raise

        return inner

    return wrapper
