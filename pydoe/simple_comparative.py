"""Module for Chapter 2."""
from scipy import stats


def t_test(df, factor_col=None, observ_col=None):
    """Wrapper for scipy.stats.ttest_ind."""

    if factor_col is None:
        factor_col = df.columns[0]

    if observ_col is None:
        observ_col = df.columns[1]

    treats = list(df[factor_col].unique())

    res = stats.ttest_ind(
        a=df[df[factor_col] == treats[0]].loc[:, observ_col].values,
        b=df[df[factor_col] == treats[1]].loc[:, observ_col].values,
        equal_var=True,  # default
        alternative='two-sided'  # default
    )

    return {"P-Value": res.pvalue}
