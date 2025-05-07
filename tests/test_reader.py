from unittest.mock import mock_open, patch

import pandas as pd

from src.reader import read_from_excel, read_from_json


@patch("src.reader.pd.read_excel")
def test_read_from_excel(mock_read_excel):
    mock_df = pd.DataFrame([{"Сумма операции": -100, "Категория": "Супермаркеты", "Описание": "Магнит"}])
    mock_read_excel.return_value = mock_df

    result = read_from_excel("our_file.xlsx")

    assert isinstance(result, list)
    assert result == [{"Сумма операции": -100, "Категория": "Супермаркеты", "Описание": "Магнит"}]


@patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
@patch("json.load")
def test_read_from_json(mock_json_load, mock_file):
    mock_json_load.return_value = {"key": "value"}

    result = read_from_json("file.json")

    assert isinstance(result, dict)
    assert result == {"key": "value"}
    mock_file.assert_called_once_with("file.json", "r", encoding="utf-8")
    mock_json_load.assert_called_once()
