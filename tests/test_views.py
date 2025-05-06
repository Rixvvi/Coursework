from unittest.mock import Mock

from src import reader, utils
from src.views import function


def test_function() -> None:
    mock_greetings = Mock(return_value="Доброе утро")
    mock_read_from_excel = Mock(return_value=[])
    mock_monthly_interval = Mock(return_value=[])
    mock_card_information = Mock(return_value=[])
    mock_top_transactions = Mock(return_value=[])
    mock_read_from_json = Mock(return_value={})
    mock_get_currencies = Mock(return_value=[])
    mock_exchange_rate = Mock(return_value=[])
    mock_get_stocks = Mock(return_value=[])
    mock_share_price = Mock(return_value=[])

    utils.greetings = mock_greetings
    reader.read_from_excel = mock_read_from_excel
    utils.monthly_interval = mock_monthly_interval
    utils.card_information = mock_card_information
    utils.top_transactions = mock_top_transactions
    reader.read_from_json = mock_read_from_json
    utils.get_currencies = mock_get_currencies
    utils.exchange_rate = mock_exchange_rate
    utils.get_stocks = mock_get_stocks
    utils.share_price = mock_share_price

    expected_func = {
        "greeting": "Доброе утро",
        "cards": [],
        "top_transactions": [],
        "currency_rates": [],
        "stock_prices": []
    }

    result = function("10.05.2024")

    assert result == expected_func
