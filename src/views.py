from src.utils import (card_information, exchange_rate, get_currencies, get_stocks, greetings, monthly_interval,
                       read_from_excel, read_from_json, share_price, top_transactions)


def function(our_date: str) -> list[dict]:
    """Функция, которая объединяет в себе весь функционал для главной страницы"""
    our_result = []

    # выводим приветствие
    first = greetings()

    # распаковываем файл с транзакциями и записываем в переменную
    second = read_from_excel("../data/operations.xlsx")
    # сортируем транзакции с начала месяца до заданной даты
    third = monthly_interval(second, our_date)

    # получаем информацию по карте
    four = card_information(third)

    # получаем топ-5 транзакций
    five = top_transactions(third)

    # читаем данные из файла
    six = read_from_json("../user_settings.json")

    # берем из файла валюту
    seven = get_currencies(six)
    # получаем ответ от api
    eight = exchange_rate(seven)

    # берем из файла акции
    nine = get_stocks(six)
    # получаем ответ от api
    ten = share_price(nine)

    our_result.append({
        "greeting": first,
        "cards": four,
        "top_transactions": five,
        "currency_rates": eight,
        "stock_prices": ten
    })

    return our_result
