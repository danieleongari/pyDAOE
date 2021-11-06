import pandas as pd
from pydaoe.anova import rcbd, latin_square, graeco_latin_square
from . import DATA_DIR


def test_example_4_1():
    """Example 4.1: Randomized Complete Block Design for the Vascular Graft Experiment."""

    df = pd.read_csv(DATA_DIR / "tab_4_3.csv")

    res = rcbd(df)  # Compare with Table 4.4

    assert res.loc["Treatements", "P-Value"] == 0.0019162997296519406


def test_example_4_2():
    """Example 4.2: Latin Square Analysis for the Rocket Propellent Experiment (with -25 shifted observations)."""

    df = pd.read_csv(DATA_DIR / "tab_4_11.csv")

    res = latin_square(df)  # Compare with Table 4.12

    assert res.loc["Treatements", "P-Value"] == 0.0025365017900521934


def test_example_4_3():
    """Example 4.3: Graeco-Latin Square Analysis for the Rocket Propellent Experiment (with -25 shifted observations)."""

    df = pd.read_csv(DATA_DIR / "tab_4_20.csv")

    res = graeco_latin_square(df)  # Compare with Table 4.21

    assert res.loc["Treatements", "P-Value"] == 0.0033436213991769547
