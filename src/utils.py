import pandas as pd


def read_from_excel(path: str) -> list[dict]:
    """Функция, которая считывает финансовые операции из XLSX и выдает список словарей с транзакциями"""
    try:
        df = pd.read_excel(path)
        data = df.to_dict(orient="records")
        return data
    except Exception as e:
        print(e.__class__.__name__)
    return []
