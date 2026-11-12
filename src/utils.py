import json


def read_file(file_path: str) -> list:
    """Принимает путь к файлу и возвращает его содержимое. Если файл не найден или пустой - возвращает пустой список"""

    try:
        with open(file_path, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
            if isinstance(data, list):
                return data
            return []
    except FileNotFoundError, json.JSONDecodeError:
        return []
