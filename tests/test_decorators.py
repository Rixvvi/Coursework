import os

import pandas as pd

from src.decorators import log


@log("test_output.csv")
def test_generate():
    return pd.DataFrame([{"name": "Alice", "age": 30}])


def test_log():
    result = test_generate()
    assert isinstance(result, pd.DataFrame)
    assert os.path.exists("test_output.csv")
    df = pd.read_csv("test_output.csv")
    assert df.iloc[0]["name"] == "Alice"
    assert df.iloc[0]["age"] == 30
    os.remove("test_output.csv")


@log("test_output.txt")
def test_nothing():
    return None


def test_log_without_output():
    result = test_nothing()
    assert result is None
