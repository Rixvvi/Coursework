from unittest.mock import Mock, patch

import pytest

from src.utils import (card_information, exchange_rate, get_currencies, get_stocks, monthly_interval, share_price,
                       top_transactions)


@pytest.fixture
def list_transactions():
    return [
        {"Дата операции": "10.04.2023 10:00:00", "Сумма операции": -100},
        {"Дата операции": "18.04.2024 12:12:00", "Сумма операции": -200},
        {"Дата операции": "29.04.2025 14:00:04", "Сумма операции": -300},
        {"Дата операции": "16.05.2020 10:00:00", "Сумма операции": -400},
        {"Дата операции": "20.05.2020 10:00:00", "Сумма операции": -400}
    ]


def test_monthly_interval_correct(list_transactions):
    user_time = '29.05.2020'
    result = monthly_interval(list_transactions, user_time)
    assert result == [
        {"Дата операции": "16.05.2020 10:00:00", "Сумма операции": -400},
        {"Дата операции": "20.05.2020 10:00:00", "Сумма операции": -400}
    ]


def test_monthly_interval_incorrect(list_transactions):
    user_time = '10.01.2000'
    result = monthly_interval(list_transactions, user_time)
    assert result == []


def test_greetings():
    mock_greetings = Mock(return_value='Добрый вечер')
    result = mock_greetings()
    assert result == 'Добрый вечер'
    mock_greetings.assert_called()


def test_card_information():
    transactions = [
        {
            "Номер карты": "1234567812345678",
            "Статус": "OK",
            "Сумма операции": -1500.75
        }
    ]
    result = card_information(transactions)
    assert result == [{
        "last_digits": "5678",
        "total_spent": 1500.75,
        "cashback": 15.01
    }]


def test_transaction_with_positive_amount():
    transactions = [
        {
            "Номер карты": "1234567812345678",
            "Статус": "OK",
            "Сумма операции": 500.00
        }
    ]
    result = card_information(transactions)
    assert result == []


def test_transaction_with_missing_card_number():
    transactions = [
        {
            "Статус": "OK",
            "Сумма операции": -100.00
        }
    ]
    result = card_information(transactions)
    assert result == []


def test_transaction_with_bad_status():
    transactions = [
        {
            "Номер карты": "1234567812345678",
            "Статус": "DECLINED",
            "Сумма операции": -200.00
        }
    ]
    result = card_information(transactions)
    assert result == []


def test_multiple_transactions():
    transactions = [
        {
            "Номер карты": "1111222233334444",
            "Статус": "OK",
            "Сумма операции": -100.00
        },
        {
            "Номер карты": "5555666677778888",
            "Статус": "OK",
            "Сумма операции": -200.00
        },
        {
            "Номер карты": "0000111122223333",
            "Статус": "OK",
            "Сумма операции": 300.00  # должно быть проигнорировано
        },
        {
            "Номер карты": "9999888877776666",
            "Статус": "DECLINED",
            "Сумма операции": -50.00  # тоже игнор
        }
    ]
    result = card_information(transactions)
    expected = [
        {"last_digits": "4444", "total_spent": 100.00, "cashback": 1.00},
        {"last_digits": "8888", "total_spent": 200.00, "cashback": 2.00}
    ]
    assert result == expected


def test_top_transactions():
    transactions = [
        {"Дата операции": "01.05.2025 12:00:00", "Сумма операции": -1000, "Категория": "Food", "Описание": "Lunch"},
        {"Дата операции": "02.05.2025 13:00:00", "Сумма операции": -2000, "Категория": "Travel", "Описание": "Taxi"},
        {"Дата операции": "03.05.2025 14:00:00", "Сумма операции": 500, "Категория": "Groceries",
         "Описание": "Market"},
        {"Дата операции": "04.05.2025 15:00:00", "Сумма операции": -3000, "Категория": "Shopping",
         "Описание": "Clothes"},
        {"Дата операции": "05.05.2025 16:00:00", "Сумма операции": 4000, "Категория": "Gifts", "Описание": "Present"},
        {"Дата операции": "06.05.2025 17:00:00", "Сумма операции": -100, "Категория": "Other", "Описание": "Misc"}
    ]
    result = top_transactions(transactions)
    assert len(result) == 5
    expected_amounts = [4000, -3000, -2000, -1000, 500]
    assert [tx["amount"] for tx in result] == expected_amounts
    assert result[0]["date"] == "05.05.2025"
    assert result[1]["date"] == "04.05.2025"
    assert result[0]["category"] == "Gifts"
    assert result[0]["description"] == "Present"


def test_top_transactions_less_than_5():
    transactions = [
        {"Дата операции": "01.05.2025 12:00:00", "Сумма операции": -1000, "Категория": "Food", "Описание": "Lunch"},
        {"Дата операции": "02.05.2025 13:00:00", "Сумма операции": 2000, "Категория": "Travel", "Описание": "Taxi"}
    ]

    result = top_transactions(transactions)
    assert len(result) == 2
    assert result[0]["amount"] == 2000
    assert result[1]["amount"] == -1000


def test_top_transactions_empty_list():
    transactions = []
    result = top_transactions(transactions)
    assert result == []


def test_top_transactions_date_format():
    transactions = [
        {"Дата операции": "31.12.2024 23:59:59", "Сумма операции": -999, "Категория": "Test", "Описание": "Test case"}
    ]
    result = top_transactions(transactions)
    assert result[0]["date"] == "31.12.2024"


@pytest.mark.parametrize(
    "accepted, expected",
    [
        # Тест 1: все успешно получено
        (
            {"user_currencies": ["Доллар", "Евро"], "user_stocks": ["МТВ", "Пятерочка", "Нокиа"]},
            ["Доллар", "Евро"]
        ),
        # Тест 2: не нашел ключ
        (
            {"currencies": ["Доллар", "Евро"], "user_stocks": ["МТВ", "Пятерочка", "Нокиа"]},
            []
        )
    ]
)
def test_get_currencies(accepted, expected):
    result = get_currencies(accepted)
    assert result == expected


@pytest.mark.parametrize(
    "accepted, expected",
    [
        # Тест 1: все успешно получено
        (
            {"user_currencies": ["Доллар", "Евро"], "user_stocks": ["МТВ", "Пятерочка", "Нокиа"]},
            ["МТВ", "Пятерочка", "Нокиа"]
        ),
        # Тест 2: не нашел ключ
        (
            {"user_currencies": ["Доллар", "Евро"], "stocks": ["МТВ", "Пятерочка", "Нокиа"]},
            []
        )
    ]
)
def test_get_stocks(accepted, expected):
    result = get_stocks(accepted)
    assert result == expected


mock_api_response = {
    "data": {
        "USD": {"code": "USD", "value": 0.011},
        "EUR": {"code": "EUR", "value": 0.012}
    }
}


@patch("src.utils.requests.get")
@patch("src.utils.os.getenv")
def test_exchange_rate_success(mock_getenv, mock_get):
    mock_getenv.return_value = "fake_api_key"

    mock_response = Mock()
    mock_response.json.return_value = mock_api_response
    mock_get.return_value = mock_response

    result = exchange_rate(["USD", "EUR"])

    assert len(result) == 2
    assert {"currency": "USD", "rate": round(1 / 0.011, 2)} in result
    assert {"currency": "EUR", "rate": round(1 / 0.012, 2)} in result

    mock_get.assert_called_once()
    mock_getenv.assert_called_once_with("API_KEY")


@patch("src.utils.requests.get", side_effect=Exception("API down"))
@patch("src.utils.os.getenv", return_value="fake_api_key")
def test_exchange_rate_exception_handling(mock_getenv, mock_get):
    result = exchange_rate(["USD"])
    assert result == []


@patch("src.utils.requests.get")
@patch("src.utils.os.getenv")
def test_exchange_rate_partial_currency(mock_getenv, mock_get):
    mock_getenv.return_value = "fake_api_key"
    mock_response = Mock()
    mock_response.json.return_value = {
        "data": {
            "USD": {"code": "USD", "value": 0.01}
        }
    }
    mock_get.return_value = mock_response

    result = exchange_rate(["USD", "EUR"])
    assert len(result) == 1
    assert result[0]["currency"] == "USD"


mock_api = {
    "Global Quote": {
        "01. symbol": "AAPL",
        "05. price": "198.5100"
    }
}


@patch("src.utils.requests.get")
@patch("src.utils.os.getenv")
def test_share_price_success(mock_getenv, mock_get):
    mock_getenv.return_value = "fake_api_key"

    mock_response = Mock()
    mock_response.json.return_value = mock_api
    mock_get.return_value = mock_response

    result = share_price(["AAPL"])

    assert result == [{"stock": "AAPL", "price": 198.51}]
    mock_get.assert_called_once()
    mock_getenv.assert_called_once_with("API")


@patch("src.utils.requests.get")
@patch("src.utils.os.getenv")
def test_share_price_no_price_data(mock_getenv, mock_get):
    mock_getenv.return_value = "fake_api_key"

    mock_response = Mock()
    mock_response.json.return_value = {"Global Quote": {}}
    mock_get.return_value = mock_response

    result = share_price(["AAPL"])
    assert result == []


@patch("src.utils.requests.get", side_effect=Exception("API failure"))
@patch("src.utils.os.getenv", return_value="fake_api_key")
def test_share_price_exception_handling(mock_getenv, mock_get):
    result = share_price(["AAPL"])
    assert result == []
