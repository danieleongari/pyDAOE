import pandas as pd
from pydoe.anova import twok_factorial
from . import DATA_DIR


def test_example_6_0():
    """Example 6.0: The 2^2 Design example in the text."""

    df = pd.read_csv(DATA_DIR / "tab_6_0.csv")

    res = twok_factorial(df)  # Compare with Table 6.1

    assert res.loc["A", "P-Value"] == 0.0000844371693000919
    assert res.loc["B", "P-Value"] == 0.0023615707965170714
    assert res.loc["AB", "P-Value"] == 0.18277648068045985


def test_example_6_1():
    """Example 6.1: 2^3 desgn on Plasma Etch experiment"""

    df = pd.read_csv(DATA_DIR / "tab_6_4.csv")

    res = twok_factorial(df)  # Compare with Table 6.6

    assert res.loc["A", "P-Value"] == 0.002678610470970536
    assert res.loc["ABC", "P-Value"] == 0.8185860578539553
