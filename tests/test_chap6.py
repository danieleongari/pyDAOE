import pandas as pd
from pydaoe.anova import twok_factorial
from . import DATA_DIR


def test_example_6_0():
    """Example 6.0: The 2^2 Design example in the text."""

    df = pd.read_csv(DATA_DIR / "tab_6_0.csv")

    res = twok_factorial(df)  # Compare with Table 6.1

    assert res.loc["A", "P-Value"] == 0.0000844371693000919
    assert res.loc["B", "P-Value"] == 0.0023615707965170714
    assert res.loc["AB", "P-Value"] == 0.18277648068045985


def test_example_6_1():
    """Example 6.1: 2^3 desgn on Plasma Etch experiment."""

    df = pd.read_csv(DATA_DIR / "tab_6_4.csv")

    res = twok_factorial(df)  # Compare with Table 6.5 and 6.6

    assert res.loc["A", "P-Value"] == 0.002678610470970536
    assert res.loc["ABC", "P-Value"] == 0.8185860578539553


def test_example_6_2():
    """Example 6.2: 2^4 desgn on Pilot Plant Filtration.
    Note: only one replica provided, not computing F0 and P-Value.
    """

    df = pd.read_csv(DATA_DIR / "tab_6_10.csv")

    res = twok_factorial(df)  # Compare with Table 6.12

    assert res.loc["A", "%Contribution"] == 32.63972953814275
    assert res.loc["B", "%Contribution"] == 0.6816075031353945
    assert res.loc["ABCD", "%Contribution"] == 0.13195921260701238


def test_example_6_2alt():
    """Example 6.2 alternative: 2^4 desgn on Pilot Plant Filtration.
    Note: discarding Factor-B, which has low %Contribution, to have 2 replicas of ACD.
    """

    df = pd.read_csv(DATA_DIR / "tab_6_10.csv")
    df = df.drop(columns=['Factor-B'])

    res = twok_factorial(df)  # Compare with Table 6.12

    assert res.loc["A", "F0"] == 83.36768802228413
    assert res.loc["A", "P-Value"] == 0.0000166669027475553
