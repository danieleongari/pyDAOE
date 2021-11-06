import pandas as pd
from pydaoe.anova import single_factor
from . import DATA_DIR


def test_example_3_1():
    """Example 3.1: The Plasma Etching Experiment"""

    df = pd.read_csv(DATA_DIR / "tab_3_1.csv")

    res = single_factor(df)  # Compare with Table 3.4

    assert res.loc["Treatements", "P-Value"] == 2.8828659084940823e-09
