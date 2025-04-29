from datetime import datetime, time
import logging

my_logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('../logs/views_logs.log', 'w')
file_formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
file_handler.setFormatter(file_formatter)
my_logger.addHandler(file_handler)
my_logger.setLevel(logging.DEBUG)


def greetings(user_time: str) -> str:
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


def monthly_interval(transactions, user_date):
    pass
