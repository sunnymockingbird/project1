import csv
import json
import logging
from json import JSONDecodeError

import pandas as pd

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("logs/utils.log", "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def read_file(file_path: str) -> list:
    """Принимает путь к файлу и возвращает его содержимое. Если файл не найден или пустой - возвращает пустой список"""
    try:
        if file_path.endswith(".json") or file_path.endswith(".csv"):
            with open(file_path, "r", encoding="utf-8") as file:
                logger.info(f"Открыт файл {file_path}")
                if file_path.endswith(".json"):
                    data = json.load(file)
                    if isinstance(data, list):
                        logger.info("Данные файла успешно прочитаны")
                        return data
                    logger.warning("Файл содержит не список, возвращен пустой список")
                    return []
                else:
                    data = list(csv.DictReader(file, delimiter=";"))
                    return data
        elif file_path.endswith(".xlsx"):
            logger.info(f"Открыт файл {file_path}")
            data = pd.read_excel(file_path).to_dict(orient="records")
            return data
        else:
            logger.warning("Не верный формат файла")
            return []
    except FileNotFoundError:
        logger.error("Файл не обнаружен, возвращен пустой список")
        return []
    except (UnicodeDecodeError, JSONDecodeError) as ex:
        logger.warning(f"Произошла ошибка {ex}, возвращен пустой список")
        return []
