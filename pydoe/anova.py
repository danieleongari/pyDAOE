"""Module for Chapter 3."""
from scipy import stats
import pandas as pd


def single_factor(df, treat_col=None, obser_col=None):
    """Single Factor experiment, also called One-Way ANOVA"""

    if treat_col is None:
        treat_col = df.columns[0]

    if obser_col is None:
        treat_col = df.columns[1]

    treats = list(df[treat_col].unique())
    treats = sorted(treats)

    n_treat = len(treats)  # a
    n_obser = len(df[df[obser_col] == treats[0]])  # n
    n_total = n_treat * n_obser  # N

    # Check if all treatements have the same number of obserrvation
    for treat in treats:
        if len(df[df[obser_col] == treat]) != n_obser:
            raise Exception("For Single-Factor test all treatments should have the same number of observations.")

    # Degree of Freedom
    dof_treat = n_treat - 1
    dof_error = n_total - n_treat
    dof_total = n_total - 1

    # Sum of Squares
    sy2id = (df.groupby(treat_col).sum()**2).sum()  # sum(y_i_dot ^ 2)
    y2dd = (df.sum(axis=1).sum(axis=0)**2).sum(axis=0)  # y_dot_dot ^ 2 = sum(yij) ^ 2
    ssy2ij = (df**2).sum(axis=1).sum(axis=0)

    ss_treat = sy2id / n_obser - y2dd / n_total
    ss_total = ssy2ij - y2dd / n_total
    ss_error = ss_total - ss_treat

    # Mean Squares
    ms_treat = ss_treat / dof_treat
    ms_error = ss_error / dof_error

    # test statistic
    f0_treat = ms_treat / ms_error
    rv = stats.f(dof_treat, dof_error)
    pval_treat = rv.sf(f0_treat)

    # Print. Table 3.3 @ pag.73, compare with Table 3.4 @ pag.74
    cols = ["Source of Variation", "Sum of Squares", "Degree of Freedom", "Mean Square", "F0", "P-value"]
    rows = [
        ["Treatements", ss_treat, dof_treat, ms_treat, f0_treat, pval_treat],
        ["Error", ss_error, dof_error, ms_error, "", ""],
        ["Total", ss_total, dof_total, "", "", ""],
    ]

    table = pd.DataFrame(rows, columns=cols)
    table = table.set_index("Source of Variation")
    return table
