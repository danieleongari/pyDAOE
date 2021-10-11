import pandas as pd
from pydoe.anova import single_factor


def example_3_0():

    df = pd.read_csv("data/tab_3_1.csv")

    res = single_factor(df)

    return res
