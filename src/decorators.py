from functools import wraps
from typing import Any, Callable, Optional

import pandas as pd


def log(file_name: Optional[str] = None) -> Any:
    """Декоратор для функций-отчетов, который записывает в файл результат, возвращаемый функцией, формирующей отчет"""
    def my_decorator(func: Callable[..., Any]) -> Any:
        @wraps(func)
        def wrapper(*args: tuple, **kwargs: dict) -> Any:
            result = func(*args, **kwargs)
            if file_name:
                if isinstance(result, pd.DataFrame):
                    result.to_csv(file_name, encoding='utf-8')
                else:
                    with open(file_name, 'w', encoding='utf-8') as file:
                        file.write(str(result))
            return result
        return wrapper
    return my_decorator
