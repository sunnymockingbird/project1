import json
import logging

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("logs/utils.log", "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def read_file(file_path: str) -> list:
    """Принимает путь к файлу и возвращает его содержимое. Если файл не найден или пустой - возвращает пустой список"""
    try:
        with open(file_path, "r", encoding="utf-8") as json_file:
            logger.info(f"Открыт файл {file_path}")
            data = json.load(json_file)
            if isinstance(data, list):
                logger.info("Данные файла успешно прочитаны")
                return data
            logger.warning("Файл содержит не список, возвращен пустой список")
            return []
    except (FileNotFoundError, json.JSONDecodeError) as ex:
        logger.error(f"Произошла ошибка {ex} возвращен пустой список")
        return []
