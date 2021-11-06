import pandas as pd
from pydoe.simple_comparative import t_test
from . import DATA_DIR


def test_example_2_cement():
    """Example in the text on the Portland Cement: assuming similar variance."""

    df = pd.read_csv(DATA_DIR / "tab_2_1.csv")

    res = t_test(df, equal_var=True, alternative='two-sided')

    assert res['P-Value'] == 0.0421967159248899


def test_example_2_1():
    """Example 2.1: nerve treatement results, assuming different variance and single tail.
    Testing if the first treatement in the table (Nerve) leads to "greater" observation than the second (Muscle).
    """

    df = pd.read_csv(DATA_DIR / "tab_2_3.csv")

    res = t_test(df, equal_var=False, alternative='greater')

    assert res['P-Value'] == 0.0072776442038488855
