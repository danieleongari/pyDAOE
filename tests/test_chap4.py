import pandas as pd
from pydoe.anova import rcbd
from . import DATA_DIR


def test_example_4_1():
    """Example 4.1: Randomized Complete Block Design for the Vascular Graft Experiment."""

    df = pd.read_csv(DATA_DIR / "tab_4_3.csv")

    res = rcbd(df)  # Compare with Table 4.4

    assert res.loc["Treatements", "P-Value"] == 0.0019162997296519406
