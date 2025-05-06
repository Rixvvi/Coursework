import logging

from src.utils import (card_information, exchange_rate, get_currencies, get_stocks, greetings, monthly_interval,
                       read_from_excel, read_from_json, share_price, top_transactions)

my_logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('../logs/views_logs.log', 'w')
file_formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
file_handler.setFormatter(file_formatter)
my_logger.addHandler(file_handler)
my_logger.setLevel(logging.DEBUG)


def function(our_date: str) -> list[dict]:
    """Функция, которая объединяет в себе весь функционал для главной страницы"""
    our_result = []

    my_logger.info("Выводим приветствие, исходя из текущего времени")
    user_greeting = greetings()

    my_logger.info("Распаковываем файл с транзакциями и записываем в переменную")
    unpacked_file = read_from_excel("../data/operations.xlsx")

    my_logger.info("Сортируем транзакции с начала месяца до заданной даты")
    sorted_transactions = monthly_interval(unpacked_file, our_date)

    my_logger.info("Получаем информацию по карте")
    bank_card_information = card_information(sorted_transactions)

    my_logger.info("Получаем топ-5 транзакций")
    top_of_our_transactions = top_transactions(sorted_transactions)

    my_logger.info("Читаем данные из файла")
    reading_file = read_from_json("../user_settings.json")

    my_logger.info("Берем из файла валюту")
    currency_from_file = get_currencies(reading_file)

    my_logger.info("Получаем ответ от api с переведенной в рубли валютой")
    currency_value = exchange_rate(currency_from_file)

    my_logger.info("Берем из файла акции")
    shares_from_file = get_stocks(reading_file)

    my_logger.info("Получаем ответ от api со стоимостью акций")
    stock_value = share_price(shares_from_file)

    our_result.append({
        "greeting": user_greeting,
        "cards": bank_card_information,
        "top_transactions": top_of_our_transactions,
        "currency_rates": currency_value,
        "stock_prices": stock_value
    })

    return our_result


if __name__ == "__main__":
    print(function("18.10.2021"))
