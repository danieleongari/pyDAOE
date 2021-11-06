import pandas as pd
from pydaoe.simple_comparative import t_test, t_test_paired
from . import DATA_DIR


def test_example_2_cement():
    """Example in the text on the Portland Cement: assuming similar variance."""

    df = pd.read_csv(DATA_DIR / "tab_2_1.csv")

    res = t_test(df, equal_var=True, alternative='two-sided')

    assert res['P-Value'] == 0.0421967159248899  # Compare with Table 2.2


def test_example_2_1():
    """Example 2.1: nerve treatement results, assuming different variance and single tail.
    Testing if the first treatement in the table (Nerve) leads to "greater" observation than the second (Muscle).
    """

    df = pd.read_csv(DATA_DIR / "tab_2_3.csv")

    res = t_test(df, equal_var=False, alternative='greater')

    assert res['P-Value'] == 0.0072776442038488855  # 0.007 in the text


def test_example_2_hardness():
    """Example in the text about the hardness of a speciment, as measured for two tips.
    Paired comparison design, with two-sided hypothesis.
    """

    df = pd.read_csv(DATA_DIR / "tab_2_6.csv")

    res = t_test_paired(df, alternative='two-sided')

    assert res['P-Value'] == 0.7976245209721027  # Compare with Table 2.7: null hypotesis NOT rejected!
