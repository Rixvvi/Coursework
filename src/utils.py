import logging
import os
from datetime import datetime, time, timedelta

import requests
from dotenv import load_dotenv

load_dotenv()

base_dir = os.path.dirname(os.path.dirname(__file__))
logs_dir = os.path.join(base_dir, "logs", "utils_logs.log")

my_logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(logs_dir, 'w', encoding="UTF-8")
file_formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
file_handler.setFormatter(file_formatter)
my_logger.addHandler(file_handler)
my_logger.setLevel(logging.DEBUG)


def monthly_interval(transactions: list[dict], user_time: str) -> list[dict]:
    """Функция, которая определяет временной промежуток от введенной пользователем даты до начала месяца"""
    result = []
    day_number = int(user_time[:2])
    stop_date = datetime.strptime(user_time, "%d.%m.%Y").date()
    start_date = stop_date - timedelta(days=(day_number - 1))
    my_logger.info("Проходимся по транзакциям и проверяем, подходит ли дата под диапазон")
    for transaction in transactions:
        transaction_date = datetime.strptime(transaction["Дата операции"], "%d.%m.%Y %H:%M:%S").date()
        if start_date <= transaction_date <= stop_date:
            result.append(transaction)
        else:
            continue
    my_logger.info("Функция отработала успешно")
    return result


def greetings() -> str:
    """Функция, которая возвращает приветствие в зависимости от времени суток"""
    try:
        my_logger.info("Приводим строку с датой к нужному формату")
        user_time = datetime.now().time()
        greets = ["Доброе утро", "Добрый день", "Добрый вечер", "Доброй ночи"]
        morning_time = time(6, 0)
        day_time = time(12, 0)
        evening_time = time(18, 0)
        night_time = time(22, 0)
        my_logger.info("Выбираем приветствие по времени суток")
        if morning_time <= user_time < day_time:
            greet = greets[0]
        elif day_time <= user_time < evening_time:
            greet = greets[1]
        elif evening_time <= user_time < night_time:
            greet = greets[2]
        else:
            greet = greets[3]
        my_logger.info("Приветствие успешно выбрано")
        return greet
    except Exception as e:
        my_logger.error("Возникла ошибка")
        print(e.__class__.__name__)


def card_information(transactions: list[dict]) -> list[dict]:
    """Функция, которая возвращает список словарей с информацией о карте:
    последние 4 цифры карты, общая сумма расходов и кэшбек"""
    result = []
    sorted_operations = []
    my_logger.info("Проверяем транзакции на то, подходят они нам или нет")
    for trans in transactions:
        card_number = trans.get("Номер карты")
        card_status = trans.get("Статус")
        card_amount = trans.get("Сумма операции")
        if not card_status == "OK":
            continue
        if card_amount >= 0:
            continue
        if not card_number:
            continue
        my_logger.info("Операция успешно добавлена")
        sorted_operations.append(trans)
    my_logger.info("Находим 4 цифры карты, сумму расходов и вычисляем кэшбек")
    for operation in sorted_operations:
        number = operation.get("Номер карты")
        amount = operation.get("Сумма операции")
        card = str(number)[-4:]
        spent = round(abs(amount), 2)
        cashback = round(spent * 0.01, 2)
        result.append({
            "last_digits": card,
            "total_spent": spent,
            "cashback": cashback
        })
        my_logger.info("Функция отработала успешно")
    return result


def top_transactions(transactions: list[dict]) -> list[dict]:
    """Функция, которая возвращает топ-5 транзакций по сумме платежа"""
    result = []
    my_logger.info("Взяты 5 наибольших отсортированных транзакций по абсолютной сумме")
    top = sorted(transactions, key=lambda x: abs(x['Сумма операции']), reverse=True)[:5]
    for i in top:
        date = i.get("Дата операции")
        date_obj = datetime.strptime(date, "%d.%m.%Y %H:%M:%S")
        date_string = date_obj.strftime("%d.%m.%Y")
        amount = i.get("Сумма операции")
        category = i.get("Категория")
        description = i.get("Описание")
        result.append({
            "date": date_string,
            "amount": amount,
            "category": category,
            "description": description
        })
    my_logger.info("Функция отработала успешно")
    return result


def exchange_rate(currency: list) -> list[dict]:
    """Функция, которая высчитывает курс валют"""
    params = ",".join(currency)
    try:
        url = "https://api.currencyapi.com/v3/latest"
        headers = {"apikey": os.getenv("API_KEY")}
        params = {
            "base_currency": "RUB",
            "currencies": params
        }
        my_logger.info("Запрос к api отправлен")
        response = requests.get(url, params=params, headers=headers, data={})
        result = response.json()
        if 'data' not in result:
            print("Ошибка в ответе от API")
        conversion = []
        for currency_code, data in result['data'].items():
            if currency_code in currency:
                my_logger.info("Запрос обработан и отформатирован")
                conversion.append({
                    "currency": currency_code,
                    "rate": round(1 / data['value'], 2)
                })
        my_logger.info("Ответы от api успешно получены и записаны")
        return conversion
    except Exception as e:
        my_logger.error("Произошла ошибка")
        print(e.__class__.__name__)
    return []


def share_price(stock: list) -> list[dict]:
    """Функция, которая высчитывает стоимость акций из S&P500"""
    symbol = stock
    finding = []
    for i in symbol:
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": i,
            "apikey": os.getenv("API")
        }
        try:
            my_logger.info("Запрос к api отправлен")
            response = requests.get(url, params=params, data={})
            result = response.json()
            if "Global Quote" in result and "05. price" in result["Global Quote"]:
                price = float(result["Global Quote"]["05. price"])
                my_logger.info("Запрос обработан и отформатирован")
                finding.append({
                    "stock": i,
                    "price": price
                })
            else:
                my_logger.info("Цена не найдена")
            my_logger.info("Ответы от api успешно получены и записаны")
        except Exception as e:
            my_logger.error("Произошла ошибка")
            print(e.__class__.__name__)
    return finding


def get_currencies(required_currency: dict) -> list:
    """Функция, которая получает валюты пользователя и возвращает их списком"""
    if "user_currencies" in required_currency:
        currency = required_currency["user_currencies"]
        return currency
    else:
        return []


def get_stocks(required_stock: dict) -> list:
    """Функция, которая получает акции пользователя и возвращает их списком"""
    if "user_stocks" in required_stock:
        stock = required_stock["user_stocks"]
        return stock
    else:
        return []
