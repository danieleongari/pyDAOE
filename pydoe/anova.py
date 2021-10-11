"""Module for tests based on the Analysis of Variance (ANOVA)."""
from scipy import stats
import pandas as pd


def _sum_y2_k(df, k, y):  #TODO: add as a function of the DataFrame
    """Sum of the squared sums over the column k.
    Typically `k` is the Factor or Block column and `y` is the column of Observations.
    """
    return (df.groupby(k).sum()[y]**2).sum()


def _y2_sum(df, y):  #TODO: add as a function of the DataFrame
    """Square of the y sum."""
    return df[y].sum()**2


def _sum_y2(df, y):  #TODO: add as a function of the DataFrame
    """Sum of y squared."""
    return (df[y]**2).sum()


def single_factor(df, factor_col=None, observ_col=None):
    """Single Factor experiment, also called One-Way ANOVA."""

    # Default format of the dataframe
    cols = [factor_col, observ_col]
    if None in cols:
        factor_col, observ_col = df.columns

    treats = list(df[factor_col].unique())
    treats = sorted(treats)

    n_treats = len(treats)  # a
    n_observ = len(df[df[factor_col] == treats[0]])  # n
    n_total = n_treats * n_observ  # N

    # Check if all treatements have the same number of observation
    for treat in treats:
        if len(df[df[factor_col] == treat]) != n_observ:
            raise NotImplementedError(
                "For Single-Factor test all treatments should have the same number of observations.")

    # Degree of Freedom
    dof_treat = n_treats - 1
    dof_error = n_total - n_treats
    dof_total = n_total - 1

    # Sum of Squares
    ss_treat = _sum_y2_k(df, factor_col, observ_col) / n_observ - _y2_sum(df, observ_col) / n_total
    ss_total = _sum_y2(df, observ_col) - _y2_sum(df, observ_col) / n_total
    ss_error = ss_total - ss_treat

    # Mean Squares
    ms_treat = ss_treat / dof_treat
    ms_error = ss_error / dof_error

    # test statistic
    f0_treat = ms_treat / ms_error
    rv = stats.f(dof_treat, dof_error)
    pval_treat = rv.sf(f0_treat)

    # Print Table 3.3
    cols = ["Source of Variation", "Sum of Squares", "Degree of Freedom", "Mean Square", "F0", "P-Value"]
    rows = [
        ["Treatements", ss_treat, dof_treat, ms_treat, f0_treat, pval_treat],
        ["Error", ss_error, dof_error, ms_error, "", ""],
        ["Total", ss_total, dof_total, "", "", ""],
    ]

    table = pd.DataFrame(rows, columns=cols)
    table = table.set_index("Source of Variation")
    return table


def rcbd(df, factor_col=None, block_col=None, observ_col=None):
    """Randomized Complete Block Design."""

    # Default format of the dataframe
    cols = [factor_col, block_col, observ_col]
    if None in cols:
        factor_col, block_col, observ_col = df.columns

    treats = list(df[factor_col].unique())
    treats = sorted(treats)

    blocks = list(df[block_col].unique())
    blocks = sorted(blocks)

    n_treats = len(treats)  # a
    n_blocks = len(blocks)  # b
    n_total = n_treats * n_blocks  # N

    # Check if all observations are provided
    if len(df) != n_total:
        raise NotImplementedError("Incomplete RCBD not implemented.")

    # Degree of Freedom
    dof_treat = n_treats - 1
    dof_block = n_blocks - 1
    dof_error = dof_treat * dof_block
    dof_total = n_total - 1

    # Sum of Squares
    ss_treat = _sum_y2_k(df, factor_col, observ_col) / n_blocks - _y2_sum(df, observ_col) / n_total
    ss_block = _sum_y2_k(df, block_col, observ_col) / n_treats - _y2_sum(df, observ_col) / n_total
    ss_total = _sum_y2(df, observ_col) - _y2_sum(df, observ_col) / n_total
    ss_error = ss_total - ss_treat - ss_block

    # Mean Squares
    ms_treat = ss_treat / dof_treat
    ms_block = ss_block / dof_block
    ms_error = ss_error / dof_error

    # test statistic
    f0_treat = ms_treat / ms_error
    rv = stats.f(dof_treat, dof_error)
    pval_treat = rv.sf(f0_treat)

    # Print Table 4.2
    cols = ["Source of Variation", "Sum of Squares", "Degree of Freedom", "Mean Square", "F0", "P-Value"]
    rows = [
        ["Treatements", ss_treat, dof_treat, ms_treat, f0_treat, pval_treat],
        ["Blocks", ss_block, dof_block, ms_block, "", ""],
        ["Error", ss_error, dof_error, ms_error, "", ""],
        ["Total", ss_total, dof_total, "", "", ""],
    ]
    table = pd.DataFrame(rows, columns=cols)
    table = table.set_index("Source of Variation")
    return table


def latin_square(df, factor_col=None, block1_col=None, block2_col=None, observ_col=None):
    """Latin square design."""

    # Default format of the dataframe
    cols = [factor_col, block1_col, block2_col, observ_col]
    if None in cols:
        factor_col, block1_col, block2_col, observ_col = df.columns

    treats = list(df[factor_col].unique())
    treats = sorted(treats)

    block1, block2 = list(df[block1_col].unique()), list(df[block2_col].unique())
    block1, block2 = sorted(block1), sorted(block2)

    # Considering equal treat, rows, cols
    n_treats = len(treats)  # p
    n_block1 = len(block1)  # "Rows", p
    n_block2 = len(block2)  # "Columns", p

    if not n_treats == n_block1 == n_block2:
        raise NotImplementedError("Incomplete Latin Square not implemented.")

    p = n_treats  # == n_block1 == n_block2 in Latin Square Design
    n_total = p**2

    # Degree of Freedom
    dof_p = p - 1
    dof_error = (p - 2) * (p - 1)
    dof_total = n_total - 1

    # Sum of Squares]
    ss_treat = _sum_y2_k(df, factor_col, observ_col) / p - _y2_sum(df, observ_col) / n_total
    ss_block1 = _sum_y2_k(df, block1_col, observ_col) / p - _y2_sum(df, observ_col) / n_total
    ss_block2 = _sum_y2_k(df, block2_col, observ_col) / p - _y2_sum(df, observ_col) / n_total
    ss_total = _sum_y2(df, observ_col) - _y2_sum(df, observ_col) / n_total
    ss_error = ss_total - ss_treat - ss_block1 - ss_block2

    # Mean Squares
    ms_treat = ss_treat / dof_p
    ms_block1 = ss_block1 / dof_p
    ms_block2 = ss_block2 / dof_p
    ms_error = ss_error / dof_error

    # test statistic
    f0_treat = ms_treat / ms_error
    rv = stats.f(dof_p, dof_error)
    pval_treat = rv.sf(f0_treat)

    # Print Table 4.10
    cols = ["Source of Variation", "Sum of Squares", "Degree of Freedom", "Mean Square", "F0", "P-Value"]
    rows = [
        ["Treatements", ss_treat, dof_p, ms_treat, f0_treat, pval_treat],
        ["Block1", ss_block1, dof_p, ms_block1, "", ""],
        ["Block2", ss_block2, dof_p, ms_block2, "", ""],
        ["Error", ss_error, dof_error, ms_error, "", ""],
        ["Total", ss_total, dof_total, "", "", ""],
    ]
    table = pd.DataFrame(rows, columns=cols)
    table = table.set_index("Source of Variation")
    return table
