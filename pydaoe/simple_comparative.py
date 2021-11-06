"""Module for simple comparative analysis."""
from scipy import stats


def t_test(df, factor_col=None, observ_col=None, equal_var='True', alternative='two-sided'):
    """Wrapper on scipy.stats.ttest_ind."""

    # Default format of the dataframe
    cols = [factor_col, observ_col]
    if None in cols:
        factor_col, observ_col = df.columns

    treats = list(df[factor_col].unique())

    res = stats.ttest_ind(
        a=df[df[factor_col] == treats[0]].loc[:, observ_col].values,
        b=df[df[factor_col] == treats[1]].loc[:, observ_col].values,
        equal_var=equal_var,  # default: True
        alternative=alternative  # default: 'two-sided'
    )

    return {"P-Value": res.pvalue}


def t_test_paired(df, factor_col=None, block_col=None, observ_col=None, alternative='two-sided'):
    """Wrapper on scipy.stats.ttest_rel."""

    # Default format of the dataframe
    cols = [factor_col, block_col, observ_col]
    if None in cols:
        factor_col, block_col, observ_col = df.columns

    treats = list(df[factor_col].unique())

    # Sort by block so that the order of observations in a and b is correct (i.e., as paired)
    df = df.sort_values(by=block_col)

    res = stats.ttest_rel(
        a=df[df[factor_col] == treats[0]].loc[:, observ_col].values,
        b=df[df[factor_col] == treats[1]].loc[:, observ_col].values,
        alternative=alternative  # default: 'two-sided'
    )

    return {"P-Value": res.pvalue}
