from datetime import datetime, time
import logging

my_logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('../logs/views_logs.log', 'w')
file_formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
file_handler.setFormatter(file_formatter)
my_logger.addHandler(file_handler)
my_logger.setLevel(logging.DEBUG)


def greetings(user_time: str) -> str:
    """Функция, которая возвращает приветствие в зависимости от времени суток"""
    try:
        my_logger.info("Приводим строку с датой к нужному формату")
        date_obj = datetime.strptime(user_time, "%H:%M:%S")
        greets = ["Доброе утро", "Добрый день", "Добрый вечер", "Доброй ночи"]
        morning_time = time(6, 0)
        day_time = time(12, 0)
        evening_time = time(18, 0)
        night_time = time(22, 0)
        my_logger.info("Выбираем приветствие по времени суток")
        if morning_time <= date_obj.time() < day_time:
            greet = greets[0]
        elif day_time <= date_obj.time() < evening_time:
            greet = greets[1]
        elif evening_time <= date_obj.time() < night_time:
            greet = greets[2]
        else:
            greet = greets[3]
        my_logger.info("Приветствие успешно выбрано")
        return greet
    except Exception as e:
        my_logger.error("Возникла ошибка")
        print(e.__class__.__name__)


def monthly_interval(transactions: list[dict]) -> list[dict]:
    """Функция, которая возвращает список словарей с информацией о карте:
    последние 4 цифры карты, общая сумма расходов и кэшбек"""
    result = []
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
    for trans in transactions:
        for card_number, card_amount in trans:
            card = card_number[-4:]
            spent = round(abs(card_amount), 2)
            cashback = round(spent * 0.01, 2)
            result.append({
                "last_digits": card,
                "total_spent": spent,
                "cashback": cashback
            })
    return result
