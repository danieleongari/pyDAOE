"""Module for Chapter 2."""
from scipy import stats


def t_test(df, treat_col, measure_col):
    """Wrapper for scipy.stats.ttest_ind."""
    treats = list(set(df[treat_col].values))
    res = stats.ttest_ind(
        a=df[df[treat_col] == treats[0]].loc[:, measure_col].values,
        b=df[df[treat_col] == treats[1]].loc[:, measure_col].values,
        equal_var=True,  # default
        alternative='two-sided'  # default
    )
    return {"P-value": res.pvalue}
