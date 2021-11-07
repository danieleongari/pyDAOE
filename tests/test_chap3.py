import pandas as pd
from pydaoe.anova import single_factor
from . import DATA_DIR


def test_example_3_1():
    """Example 3.1: The Plasma Etching Experiment"""

    df = pd.read_csv(DATA_DIR / "tab_3_1.csv")

    res = single_factor(df)  # Compare with Table 3.4

    assert res.loc["Treatements", "P-Value"] == 2.8828659084940823e-09


def test_example_3_10():
    """Example 3.10: Random Factor experiment on textile strength."""

    df = pd.read_csv(DATA_DIR / "tab_3_18.csv")

    res = single_factor(df)  # Compare with Table 3.19

    assert res.loc["Treatements", "P-Value"] == 0.00018779198099318047  # <0.001 in the text
