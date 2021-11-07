"""Module for simple comparative analysis."""
from scipy import stats
from statsmodels.stats import weightstats


def t_test(df, factor_col=None, observ_col=None, equal_var=True, alternative='two-sided'):
    """Wrapper on scipy.stats.ttest_ind."""

    # Default format of the dataframe
    cols = [factor_col, observ_col]
    if None in cols:
        factor_col, observ_col = df.columns

    treats = list(df[factor_col].unique())

    res = stats.ttest_ind(
        a=df[df[factor_col] == treats[0]].loc[:, observ_col].values,
        b=df[df[factor_col] == treats[1]].loc[:, observ_col].values,
        equal_var=equal_var,  # bool, default: True
        alternative=alternative  # [two-sided, greater, less], default: 'two-sided'
    )

    return {"P-Value": res.pvalue}


def t_test_statsmodels(df, factor_col=None, observ_col=None, equal_var='pooled', alternative='two-sided'):
    """Same as t_test, but using statsmodels instead.
    I could not find a statsmodels alternative also for ttest_rel: weightstats.ttost_paired is not the same!
    """

    # Default format of the dataframe
    cols = [factor_col, observ_col]
    if None in cols:
        factor_col, observ_col = df.columns

    treats = list(df[factor_col].unique())

    res = weightstats.ttest_ind(
        x1=df[df[factor_col] == treats[0]].loc[:, observ_col].values,  # `a` in scipy.stats.ttest_ind
        x2=df[df[factor_col] == treats[1]].loc[:, observ_col].values,  # `b` in scipy.stats.ttest_ind
        usevar=equal_var,  # [pooled, unequal], for same/different stdev. `equal_var` in scipy.stats.ttest_ind
        alternative=alternative,  #[two-sided, larger, smaller], in scipy.stats.ttest_ind: [two-sided, greater, less]
    )

    return {"t-stats": res[0], "P-Value": res[1], "DoF": res[2]}


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
        alternative=alternative  # [two-sided, greater, less], default: 'two-sided'
    )

    return {"P-Value": res.pvalue}
