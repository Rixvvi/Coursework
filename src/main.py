import pandas as pd

from src.reader import read_from_excel
from src.reports import spending_by_category
from src.services import get_search_numbers, get_search_str
from src.views import function


def main_function() -> str:
    """Функция, которая объединяет в себе весь написанный функционал в одно целое"""

    print("Транзакции будут выведены с начала месяца до вашей введенной даты включительно")
    user_input = input("Введите дату в формате %d-%m-%Y: ")
    a = function(user_input)
    print(a)

    unpacking = read_from_excel("../data/operations.xlsx")

    print("Транзакции будут отсортированы по вашему вводу, который будет найден в категориях или описании")
    user_input = input("Введите ключевое слово или словосочетание, по которому хотите найти транзакции: ")
    b = get_search_str(unpacking, user_input)
    print(b)

    print("Транзакции будут отсортированы по наличию номера телефона в описании")
    с = get_search_numbers(unpacking)
    print(с)

    print("Транзакции будут отсортированы по введенной вами категории и дате (необязательный параметр)")
    user_input = input("Введите название категории, по которой хотите найти транзакции: ")
    your_input = input("Введите дату для получения транзакция за последние три месяца: ")
    new_list = pd.DataFrame(unpacking)
    d = spending_by_category(new_list, user_input, your_input)
    print(d)

    u = "Работа функции завершена"

    return u
