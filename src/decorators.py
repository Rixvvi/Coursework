from functools import wraps
import pandas as pd


def log(file_name):
    def my_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if isinstance(result, pd.DataFrame):
                result.to_csv(file_name, encoding='utf-8')
            else:
                with open(file_name, 'w', encoding='utf-8') as file:
                    file.write(str(result))
            return result
        return wrapper
    return my_decorator
