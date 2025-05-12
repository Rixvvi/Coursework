import logging
import os

from src import reader, utils

base_dir = os.path.dirname(os.path.dirname(__file__))
logs_dir = os.path.join(base_dir, "logs", "views_logs.log")

my_logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(logs_dir, 'w', encoding="UTF-8")
file_formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
file_handler.setFormatter(file_formatter)
my_logger.addHandler(file_handler)
my_logger.setLevel(logging.DEBUG)


def function(our_date: str) -> dict:
    """Функция, которая объединяет в себе весь функционал для главной страницы"""
    my_logger.info("Выводим приветствие, исходя из текущего времени")
    user_greeting = utils.greetings()

    my_logger.info("Распаковываем файл с транзакциями и записываем в переменную")
    unpacked_file = reader.read_from_excel("../data/operations.xlsx")

    my_logger.info("Сортируем транзакции с начала месяца до заданной даты")
    sorted_transactions = utils.monthly_interval(unpacked_file, our_date)

    my_logger.info("Получаем информацию по карте")
    bank_card_information = utils.card_information(sorted_transactions)

    my_logger.info("Получаем топ-5 транзакций")
    top_of_our_transactions = utils.top_transactions(sorted_transactions)

    my_logger.info("Читаем данные из файла")
    reading_file = reader.read_from_json("../user_settings.json")

    my_logger.info("Берем из файла валюту")
    currency_from_file = utils.get_currencies(reading_file)

    my_logger.info("Получаем ответ от api с переведенной в рубли валютой")
    currency_value = utils.exchange_rate(currency_from_file)

    my_logger.info("Берем из файла акции")
    shares_from_file = utils.get_stocks(reading_file)

    my_logger.info("Получаем ответ от api со стоимостью акций")
    stock_value = utils.share_price(shares_from_file)

    return {
        "greeting": user_greeting,
        "cards": bank_card_information,
        "top_transactions": top_of_our_transactions,
        "currency_rates": currency_value,
        "stock_prices": stock_value}


if __name__ == "__main__":
    print(function("18.10.2021"))
