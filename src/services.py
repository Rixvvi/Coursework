import re
import json
import logging

my_logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('../logs/services_logs.log', 'w')
file_formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
file_handler.setFormatter(file_formatter)
my_logger.addHandler(file_handler)
my_logger.setLevel(logging.DEBUG)


def get_search_str(transactions: list[dict], string_search: str) -> list[dict]:
    """Функция, которая принимает строку пользователя и возвращает JSON-ответ с транзакциями,
    в описании которых находится переданная пользователем строка"""
    result = []
    try:
        my_logger.info("Начинаем поиск транзакций по строке, введенной пользователем")
        for i in transactions:
            category = re.search(rf"{string_search}", i.get("Категория", ""), flags=re.IGNORECASE)
            description = re.search(rf"{string_search}", i.get("Описание", ""), flags=re.IGNORECASE)
            if category or description:
                result.append(i)
        my_logger.info("Поиск транзакций успешно завершен")
    except Exception as e:
        my_logger.error("Возникла ошибка")
        print(e.__class__.__name__)
    try:
        with open("dtyd.json", "w", encoding="utf-8") as file:
            json.dump(result, file)
    except Exception as e:
        my_logger.error("Возникла ошибка при попытке записи в файл")
        print(e.__class__.__name__)
    return result


def get_search_numbers(transactions: list[dict]) -> list[dict]:
    """Функция, которая принимает список словарей с транзакциями и возвращает JSON-ответ с транзакциями,
        в описании которых находится номер телефона"""
    result = []
    pattern = re.compile(r"\+\d+ \d+ \d+-\d+-\d+$")
    my_logger.info("Начинаем поиск транзакций по описаниям, в которых есть номера телефонов")
    try:
        for i in transactions:
            if re.search(pattern, i.get("Описание", "")):
                result.append(i)
        my_logger.info("Поиск транзакций по наличию номера телефона завершен")
    except Exception as e:
        my_logger.error("Возникла ошибка")
        print(e.__class__.__name__)
    try:
        with open("dp.json", "w", encoding="utf-8") as file:
            json.dump(result, file)
    except Exception as e:
        my_logger.error("Возникла ошибка при попытке записи в файл")
        print(e.__class__.__name__)
    return result
