import pandas as pd
from pydoe.anova import two_factor_factorial
from . import DATA_DIR


def test_example_5_1():
    """Example 5.1: The Battery Design Experiment"""

    df = pd.read_csv(DATA_DIR / "tab_5_1.csv")

    res = two_factor_factorial(df)  # Compare with Table 5.5

    assert res.loc["Factor-1", "P-Value"] == 0.001976082590907497
    assert res.loc["Factor-2", "P-Value"] == 1.9085958974331855e-07
    assert res.loc["Interaction", "P-Value"] == 0.018611168188941943
