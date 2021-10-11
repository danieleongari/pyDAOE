import pandas as pd
from pydoe.simple_comparative import t_test
from . import DATA_DIR


def test_example_2_0():
    """Example in the text."""

    df = pd.read_csv(DATA_DIR / "tab_2_1.csv")

    res = t_test(df)

    assert res['P-Value'] == 0.0421967159248899
