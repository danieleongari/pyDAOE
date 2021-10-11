"""Module for tests based on the Analysis of Variance (ANOVA)."""
from scipy import stats
import pandas as pd


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
    sy2id = (df.groupby(factor_col).sum()[observ_col]**2).sum()
    y2dd = df[observ_col].sum()**2
    ssy2ij = (df[observ_col]**2).sum()

    ss_treat = sy2id / n_observ - y2dd / n_total
    ss_total = ssy2ij - y2dd / n_total
    ss_error = ss_total - ss_treat

    # Mean Squares
    ms_treat = ss_treat / dof_treat
    ms_error = ss_error / dof_error

    # test statistic
    f0_treat = ms_treat / ms_error
    rv = stats.f(dof_treat, dof_error)
    pval_treat = rv.sf(f0_treat)

    # Print. Table 3.3
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
    sy2id = (df.groupby(factor_col).sum()[observ_col]**2).sum()  # sum(y_i_dot ^ 2)
    sy2dj = (df.groupby(block_col).sum()[observ_col]**2).sum()  # sum(y_dot_j ^ 2)
    y2dd = df[observ_col].sum()**2  # y_dot_dot ^ 2 = sum(yij) ^ 2
    ssy2ij = (df[observ_col]**2).sum()

    ss_treat = sy2id / n_blocks - y2dd / n_total
    ss_block = sy2dj / n_treats - y2dd / n_total
    ss_total = ssy2ij - y2dd / n_total
    ss_error = ss_total - ss_treat - ss_block

    # Mean Squares
    ms_treat = ss_treat / dof_treat
    ms_block = ss_block / dof_block
    ms_error = ss_error / dof_error

    # test statistic
    f0_treat = ms_treat / ms_error
    rv = stats.f(dof_treat, dof_error)
    pval_treat = rv.sf(f0_treat)

    # Print. Table 4.2 @ pag.140, compare with Table 4.4 @ pag.141
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
