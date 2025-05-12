import json
import logging
import os

import pandas as pd

base_dir = os.path.dirname(os.path.dirname(__file__))
logs_dir = os.path.join(base_dir, "logs", "views_logs.log")

my_logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(logs_dir, 'w', encoding="UTF-8")
file_formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
file_handler.setFormatter(file_formatter)
my_logger.addHandler(file_handler)
my_logger.setLevel(logging.DEBUG)


def read_from_excel(path: str) -> list[dict]:
    """Функция, которая считывает финансовые операции из XLSX и выдает список словарей с транзакциями"""
    try:
        df = pd.read_excel(path)
        data = df.to_dict(orient="records")
        my_logger.info("Все прошло успешно, данные из файла записаны в переменную")
        return data
    except Exception as e:
        my_logger.error("Произошла ошибка")
        print(e.__class__.__name__)
    return []


def read_from_json(path: str) -> dict:
    """Функция, которая считывает информацию из JSON и выдает ее"""
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
            my_logger.info("Все прошло успешно, данные из файла записаны в переменную")
            return data
    except Exception as e:
        my_logger.error("Произошла ошибка")
        print(e.__class__.__name__)
    return {}
