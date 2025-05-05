import logging
from datetime import datetime
from typing import Optional

import pandas as pd

from src.decorators import log

my_logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('../logs/reports_logs.log', 'w')
file_formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
file_handler.setFormatter(file_formatter)
my_logger.addHandler(file_handler)
my_logger.setLevel(logging.DEBUG)


@log('result.txt')
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Функция, которая возвращает траты по заданной категории за последние три месяца от переданной даты"""
    try:
        my_logger.info('Проверяем, указана ли дата')
        if not date:
            stop_date = datetime.now()
        else:
            stop_date = datetime.strptime(date, "%d.%m.%Y")
        start_date = stop_date - pd.Timedelta(days=90)

        columns = ['Дата платежа', 'Сумма операции', 'Категория']
        my_logger.info('Проверяем наличие необходимых нам колонок')
        for i in columns:
            if i not in transactions.columns:
                continue
        transactions["Дата платежа"] = pd.to_datetime(transactions["Дата платежа"], format="%d.%m.%Y")
        a = (transactions["Дата платежа"] >= start_date) & (transactions["Дата платежа"] <= stop_date)
        b = transactions["Категория"] == category
        c = transactions["Сумма операции"] < 0
        filtered_transactions = transactions[a & b & c]
        if len(filtered_transactions) == 0:
            result = pd.DataFrame({
                "Категория": [category],
                "Сумма трат": ["Не найдено"]
            })
            my_logger.info("Подходящих операций не найдено")
            return result
        spending = filtered_transactions["Сумма операции"].abs()
        result = pd.DataFrame({
            "Категория": [category] * len(spending),
            "Сумма трат": spending
        })
        my_logger.info('Все успешно')
        return result
    except Exception as e:
        my_logger.error('Произошла ошибка')
        print(e.__class__.__name__)
