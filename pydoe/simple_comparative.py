"""Module for Chapter 2."""
from scipy import stats


def t_test(df, factor_col=None, observ_col=None):
    """Wrapper for scipy.stats.ttest_ind."""

    # Default format of the dataframe
    cols = [factor_col, observ_col]
    if None in cols:
        factor_col, observ_col = df.columns

    treats = list(df[factor_col].unique())

    res = stats.ttest_ind(
        a=df[df[factor_col] == treats[0]].loc[:, observ_col].values,
        b=df[df[factor_col] == treats[1]].loc[:, observ_col].values,
        equal_var=True,  # default
        alternative='two-sided'  # default
    )

    return {"P-Value": res.pvalue}
